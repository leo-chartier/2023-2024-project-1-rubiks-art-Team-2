# If modifying the scopes, delete the file token.json.

import json
import os
try:
    from bs4 import BeautifulSoup, Tag
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
    from PIL import Image
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.remote.webelement import WebElement
    from selenium.webdriver.support.ui import WebDriverWait
except ImportError:
    os.system("python3 -m pip install --upgrade beautifulsoup4 selenium google-api-python-client google-auth-httplib2 google-auth-oauthlib")
    print("Dependencies have been installed. Please execute the program again.")
    exit()





config = {}

class Face:
    def __init__(self, colors: list[str], moves: str) -> None:
        assert len(colors) == 9
        self.colors = colors
        self.moves = moves
    
    def __repr__(self) -> str:
        return "|".join(self.colors) + " " + self.moves

def format_coord(x: int, y: int) -> str:
    number = x + 1
    text = ""
    while number > 0:
        remainder = (number - 1) % 26
        text = chr(65 + remainder) + text
        number = (number - 1) // 26
    return f"{text}{y + 1}"

# Adapted from https://gist.github.com/florentbr/349b1ab024ca9f3de56e6bf8af2ac69e
JS_DROP_FILES = """
const element = arguments[0];
const bounds = element.getBoundingClientRect();
const centerX = bounds.left + (bounds.width / 2);
const centerY = bounds.top + (bounds.height / 2);

let fileInput = document.createElement('INPUT');
fileInput.setAttribute('type', 'file');
fileInput.onchange = (event) => {
    fileInput.parentElement.removeChild(fileInput);
    event.stopPropagation();
    let dragEvent = document.createEvent('DragEvent');
    dragEvent.initMouseEvent('drop', true, true, document.defaultView, 0, 0, 0, centerX, centerY, false, false, false, false, 0, null);
    Object.setPrototypeOf(dragEvent, null);
    dragEvent.dataTransfer = { constructor: DataTransfer, files: fileInput.files };
    Object.setPrototypeOf(dragEvent, DragEvent.prototype);
    element.dispatchEvent(dragEvent);
};
document.documentElement.appendChild(fileInput);
fileInput.getBoundingClientRect();
return fileInput;
"""

def convert_image(path: str) -> BeautifulSoup:
    abspath = os.path.abspath(path)

    # We check that the colors and size are correct
    img = Image.open(path).convert("RGB")
    if img.width % 3 != 0 or img.height % 3 != 0:
        raise ValueError(f"Wrong image size (must be multiples of 3, was {img.size})")
    colors = list(map(lambda x: x[1], img.getcolors()))
    available_colors = list(map(tuple, config["converter_colors"]))
    if set(colors).difference(available_colors):
        print(set(colors).difference(available_colors))
        raise ValueError(f"Invalid color found (can be {available_colors}, found {colors})")

    # We start the webdriver that will do the conversion
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    driver = webdriver.Chrome(options)
    driver.get("https://bestsiteever.ru/algs_for_mosaic/")

    # We drop in the selected file
    droparea = driver.find_element(By.CLASS_NAME, "drop-area")
    temp_input: WebElement = driver.execute_script(JS_DROP_FILES, droparea)
    temp_input._execute("sendKeysToElement", {"text": abspath})

    # We start and wait for the conversion
    start: WebElement = WebDriverWait(driver, 3).until(lambda d: d.find_element(By.CLASS_NAME, "btn-primary"))
    start.click()
    WebDriverWait(driver, 30).until(lambda d: d.find_element(By.CLASS_NAME, "cube-square"))

    # We return the content as a soup
    soup = BeautifulSoup(driver.page_source, features="html.parser")
    driver.quit()
    return soup

def extract_moves(soup: BeautifulSoup) -> list[list[Face]]:
    container = soup.find(class_="row px-2 py-1").parent
    moves: list[list[Face]] = []
    
    # The rows are split by headers indicating the row number
    rows: list[list[Tag]] = []
    for tag in container.children:
        if tag.name == "h2":
            rows.append([])
        else:
            rows[-1].append(tag)
    
    # Extract the colors and the moves
    for row in reversed(rows):
        moves.append([])
        for column in row:
            moves[-1].append(Face(
                [cubelet["style"].split(" ")[1][:-1] for cubelet in column.contents[1].find_all(class_="cube-square")],
                column.contents[2].text
            ))

    assert len(moves) % 3 == 0
    assert len(moves[0]) % 3 == 0
    assert len(set(len(row) for row in moves)) == 1

    return moves

def write_to_spreadsheets(moves: list[list[Face]]):
    creds = None
    # token.json is automatically created the first time
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', config["scopes"])
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request()) # If this fails, delete token.json
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', config["scopes"])
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    requests = [
        ## Fresco
        # Clear the formatting (colors)
        {"updateCells": {
            "range": {"sheetId": config["fresco_id"]},
            "fields": "*"
        }},
        # Clear the borders
        {"updateBorders": {
            "range": {
                "sheetId": config["fresco_id"],
            },
            "top": {"style": "NONE"},
            "bottom": {"style": "NONE"},
            "left": {"style": "NONE"},
            "right": {"style": "NONE"},
            "innerHorizontal": {"style": "NONE"},
            "innerVertical": {"style": "NONE"},
        }},
        # Resize the image
        {"updateSheetProperties": {
            "properties": {
                "gridProperties": {"rowCount": len(moves) * 3, "columnCount": len(moves[0]) * 3},
                "sheetId": config["fresco_id"]
            },
            "fields": "gridProperties"
        }},
        # Resize the column width
        {"updateDimensionProperties": {
            "range": {"sheetId": config["fresco_id"], "dimension": "COLUMNS"},
            "properties": {"pixelSize": config["cell_size"]},
            "fields": "pixelSize"
        }},
        # Resize the row height
        {"updateDimensionProperties": {
            "range": {"sheetId": config["fresco_id"], "dimension": "ROWS"},
            "properties": {"pixelSize": config["cell_size"]},
            "fields": "pixelSize"
        }},

        ## Instructions
        # Clear the formatting (colors)
        {"updateCells": {
            "range": {"sheetId": config["moves_id"]},
            "fields": "*"
        }},
        # Resize the sheet
        {"updateSheetProperties": {
            "properties": {
                "gridProperties": {"rowCount": len(moves) * len(moves[0]) + 1, "columnCount": 5},
                "sheetId": config["moves_id"]
            },
            "fields": "gridProperties"
        }},
        # Freeze the header
        {"updateSheetProperties": {
            "properties": {
                "gridProperties": {"frozenRowCount": 1},
                "sheetId": config["moves_id"]
            },
            "fields": "gridProperties.frozenRowCount"
        }}
    ]

    # Set the color for every pixel
    for i in range(len(moves) * 3):
        row = moves[i // 3]
        for j in range(len(row) * 3):
            face = row[j // 3]
            color = face.colors[3 * (i % 3) + (j % 3)]
            requests.append({"updateCells": {
                "range": {
                    "sheetId": config["fresco_id"],
                    "startRowIndex": i,
                    "endRowIndex": i + 1,
                    "startColumnIndex": j,
                    "endColumnIndex": j + 1
                },
                "rows": [{"values": [{"userEnteredFormat": {"backgroundColor": config["colors"][color]}}]}],
                "fields": "userEnteredFormat.backgroundColor"
            }})
    
    # Set the border for every cube and section
    for i in range(len(moves)):
        for j in range(len(moves[i])):
            requests.append({"updateBorders": {
                "range": {
                    "sheetId": config["fresco_id"],
                    "startRowIndex": 3 * i,
                    "endRowIndex": 3 * i + 3,
                    "startColumnIndex": 3 * j,
                    "endColumnIndex": 3 * j + 3
                },
                "top": {"style": "SOLID", "width": 1, "color": {}},
                "bottom": {"style": "SOLID", "width": 1, "color": {}},
                "left": {"style": "SOLID", "width": 1, "color": {}},
                "right": {"style": "SOLID", "width": 1, "color": {}},
            }})
    w, h, ox, oy = config["sections"]["width"]*3, config["sections"]["height"]*3, config["sections"]["offsetX"], config["sections"]["offsetY"]
    for i in range((oy-h) % h, len(moves) * 3, h):
        for j in range((ox-w) % w, len(moves[i//3]) * 3, w):
            requests.append({"updateBorders": {
                "range": {
                    "sheetId": config["fresco_id"],
                    "startRowIndex": max(i, 0),
                    "endRowIndex": min(i + h, len(moves) * 3),
                    "startColumnIndex": max(j, 0),
                    "endColumnIndex": min(j + w, len(moves[i//3]) * 3)
                },
                "top": {"style": "SOLID_THICK", "width": 1, "color": {}},
                "bottom": {"style": "SOLID_THICK", "width": 1, "color": {}},
                "left": {"style": "SOLID_THICK", "width": 1, "color": {}},
                "right": {"style": "SOLID_THICK", "width": 1, "color": {}},
            }})

    # Set the instructions
    i = 0
    rows_text = [("Coords", "Status", "Front", "Up", "Moves")]
    for y, row in enumerate(reversed(moves)):
        for x, move in enumerate(row):
            i += 1
            front = config["default_front"]
            up = config["default_up"]
            # TODO: Correct orientation
            front_rgb = config["colors"][front]
            up_rgb = config["colors"][up]
            rows_text.append((format_coord(x, y), "0", front, up, move.moves))
            requests.append({
                "updateCells": {
                    "rows": [
                        {"values": [
                            {"userEnteredFormat": {"backgroundColor": front_rgb}}
                        ]}
                    ],
                    "fields": '*',
                    "range": {
                        "sheetId": config["moves_id"],
                        "startRowIndex": i,
                        "endRowIndex": i + 1,
                        "startColumnIndex": 2,
                        "endColumnIndex": 3
                    }
                }
            })
            requests.append({
                "updateCells": {
                    "rows": [
                        {"values": [
                            {"userEnteredFormat": {"backgroundColor": up_rgb}}
                        ]}
                    ],
                    "fields": '*',
                    "range": {
                        "sheetId": config["moves_id"],
                        "startRowIndex": i,
                        "endRowIndex": i + 1,
                        "startColumnIndex": 3,
                        "endColumnIndex": 4
                    }
                }
            })
    

    
    try:
        # Run it all
        service = build('sheets', 'v4', credentials=creds)
        sheets = service.spreadsheets()
        sheets_names_by_id = {
            sheet["properties"]["sheetId"]: sheet["properties"]["title"]
            for sheet in sheets.get(spreadsheetId=config["spreadsheet_id"]).execute()["sheets"]
        }
        sheets.batchUpdate(
            spreadsheetId=config["spreadsheet_id"],
            body={"requests": requests}
        ).execute()
        sheets.values().update(
            spreadsheetId=config["spreadsheet_id"],
            range=sheets_names_by_id[config["moves_id"]] + "!A:E",
            valueInputOption="USER_ENTERED",
            body={"values": rows_text}
        ).execute()

    except HttpError as err:
        print(err)



def main():
    global config
    os.chdir(os.path.dirname(__file__))
    with open("config.json", "r") as f:
        config = json.load(f)
    soup = convert_image(config["image_path"])
    moves = extract_moves(soup)
    write_to_spreadsheets(moves)

if __name__ == "__main__":
    main()
