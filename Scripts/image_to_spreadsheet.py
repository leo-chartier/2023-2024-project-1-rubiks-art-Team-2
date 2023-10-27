# If modifying the scopes or if the token is expired, delete the file token.json.

# Note: Some modifications have been made to adapt to the specifications of team 3.

# Notation for the moves configuration:
"""
   123
   4U6
   789
123123123123
4L64F64R64B6
789789789789
   123
   4D6
   789
(middle of a face is 5)

Uppercase letter: Single layer
Lowercase letter: Double layer (Face layer + middle layer)
Only a letter: 90° clockwise
Letter with apostrophe: 90° counterclockwise
Letter with 2: 180° rotation

Example:
A 90° counterclockwise rotation of the left face would be written as L'
One of the moves from this rotation is the facelet from U1 moving to B9
"""



# TODO: Fix other TODOs and add connection to robot
# TODO: Split the code in multiple files and add documentation

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





DEFAULT_CONFIG = {
    "image_path": "", # Path to the image you want to convert
    "spreadsheet_id": "", # ID of the spreadsheet to use
    "scopes": ["https://www.googleapis.com/auth/spreadsheets"],
    "fresco_id": -1, # ID of the sheet with the fresco preview
    "moves_id": -1, # ID of the sheet with the list of moves for each cube
    "cell_size": 5, # Width and height of a cell on the preview
    "sections": {
        # Dividing the work in smaller parts, number are in cubes
        "width": 5,
        "height": 5,
        "offsetX": 0,
        "offsetY": 0
    },
    "default_cube": {
        # Defined by https://bestsiteever.ru/algs_for_mosaic/
        "F": "green",
        "B": "blue",
        "U": "white",
        "D": "yellow",
        "L": "orange",
        "R": "red"
    },
    "converter_colors": [
        # Defined by https://bestsiteever.ru/algs_for_mosaic/
        [255, 255, 255],
        [255, 255,   0],
        [255,   0,   0],
        [  0, 255,   0],
        [  0,   0, 255],
        [255, 153,   0]
    ],
    "colors": {
        "white":  {"red": 1, "green": 1,    "blue": 1},
        "yellow": {"red": 1, "green": 1,    "blue": 0},
        "blue":   {"red": 0, "green": 0.5,  "blue": 1},
        "green":  {"red": 0, "green": 0.75, "blue": 0},
        "red":    {"red": 1, "green": 0,    "blue": 0},
        "orange": {"red": 1, "green": 0.5,  "blue": 0}
    },
    "moves": {
        "F": {"F1": "F3", "F2": "F6", "F3": "F9", "F4": "F2", "F6": "F8", "F7": "F1", "F8": "F4", "F9": "F7", "U7": "R1", "U8": "R4", "U9": "R7", "R1": "D1", "R4": "D2", "R7": "D3", "D1": "L3", "D2": "L6", "D3": "L9", "L3": "U7", "L6": "U8", "L9": "U9"},
        "B": {"B1": "B3", "B2": "B6", "B3": "B9", "B4": "B2", "B6": "B8", "B7": "B1", "B8": "B4", "B9": "B7", "U3": "L1", "U2": "L4", "U1": "L7", "L1": "D9", "L4": "D8", "L7": "D7", "D9": "R9", "D8": "R6", "D7": "R3", "R9": "U3", "R6": "U2", "R3": "U1"},
        "U": {"U1": "U3", "U2": "U6", "U3": "U9", "U4": "U2", "U6": "U8", "U7": "U1", "U8": "U4", "U9": "U7", "B3": "R3", "B2": "R2", "B1": "R1", "R3": "F3", "R2": "F2", "R1": "F1", "F3": "L3", "F2": "L2", "F1": "L1", "L3": "B3", "L2": "B2", "L1": "B1"},
        "D": {"D1": "D3", "D2": "D6", "D3": "D9", "D4": "D2", "D6": "D8", "D7": "D1", "D8": "D4", "D9": "D7", "F7": "R7", "F8": "R8", "F9": "R9", "R7": "B7", "R8": "B8", "R9": "B9", "B7": "L7", "B8": "L8", "B9": "L9", "L7": "F7", "L8": "F8", "L9": "F9"},
        "L": {"L1": "L3", "L2": "L6", "L3": "L9", "L4": "L2", "L6": "L8", "L7": "L1", "L8": "L4", "L9": "L7", "U1": "F1", "U4": "F4", "U7": "F7", "F1": "D1", "F4": "D4", "F7": "D7", "D1": "B9", "D4": "B6", "D7": "B3", "B9": "U1", "B6": "U4", "B3": "U7"},
        "R": {"R1": "R3", "R2": "R6", "R3": "R9", "R4": "R2", "R6": "R8", "R7": "R1", "R8": "R4", "R9": "R7", "U9": "B1", "U6": "B4", "U3": "B7", "B1": "D9", "B4": "D6", "B7": "D3", "D9": "F9", "D6": "F6", "D3": "F3", "F9": "U9", "F6": "U6", "F3": "U3"},
        "M": {"U2": "F2", "U5": "F5", "U8": "F8", "F2": "D2", "F5": "D5", "F8": "D8", "D2": "B8", "D5": "B5", "D8": "B2", "B8": "U2", "B5": "U5", "B2": "U8"},
        "E": {"F4": "R4", "F5": "R5", "F6": "R6", "R4": "B4", "R5": "B5", "R6": "B6", "B4": "L4", "B5": "L5", "B6": "L6", "L4": "F4", "L5": "F5", "L6": "F6"},
        "S": {"U4": "R2", "U5": "R5", "U6": "R8", "R2": "D6", "R5": "D5", "R8": "D4", "D6": "L8", "D5": "L5", "D4": "L2", "L8": "U4", "L5": "U5", "L2": "U6"},
        "x": {"L3": "L1", "L6": "L2", "L9": "L3", "L2": "L4", "L8": "L6", "L1": "L7", "L4": "L8", "L7": "L9", "F1": "U1", "F4": "U4", "F7": "U7", "D1": "F1", "D4": "F4", "D7": "F7", "B9": "D1", "B6": "D4", "B3": "D7", "U1": "B9", "U4": "B6", "U7": "B3", "F2": "U2", "F5": "U5", "F8": "U8", "D2": "F2", "D5": "F5", "D8": "F8", "B8": "D2", "B5": "D5", "B2": "D8", "U2": "B8", "U5": "B5", "U8": "B2", "R1": "R3", "R2": "R6", "R3": "R9", "R4": "R2", "R6": "R8", "R7": "R1", "R8": "R4", "R9": "R7", "U9": "B1", "U6": "B4", "U3": "B7", "B1": "D9", "B4": "D6", "B7": "D3", "D9": "F9", "D6": "F6", "D3": "F3", "F9": "U9", "F6": "U6", "F3": "U3"},
        "y": {"U1": "U3", "U2": "U6", "U3": "U9", "U4": "U2", "U6": "U8", "U7": "U1", "U8": "U4", "U9": "U7", "B3": "R3", "B2": "R2", "B1": "R1", "R3": "F3", "R2": "F2", "R1": "F1", "F3": "L3", "F2": "L2", "F1": "L1", "L3": "B3", "L2": "B2", "L1": "B1", "R4": "F4", "R5": "F5", "R6": "F6", "B4": "R4", "B5": "R5", "B6": "R6", "L4": "B4", "L5": "B5", "L6": "B6", "F4": "L4", "F5": "L5", "F6": "L6", "D3": "D1", "D6": "D2", "D9": "D3", "D2": "D4", "D8": "D6", "D1": "D7", "D4": "D8", "D7": "D9", "R7": "F7", "R8": "F8", "R9": "F9", "B7": "R7", "B8": "R8", "B9": "R9", "L7": "B7", "L8": "B8", "L9": "B9", "F7": "L7", "F8": "L8", "F9": "L9"},
        "z": {"F1": "F3", "F2": "F6", "F3": "F9", "F4": "F2", "F6": "F8", "F7": "F1", "F8": "F4", "F9": "F7", "U7": "R1", "U8": "R4", "U9": "R7", "R1": "D1", "R4": "D2", "R7": "D3", "D1": "L3", "D2": "L6", "D3": "L9", "L3": "U7", "L6": "U8", "L9": "U9", "U4": "R2", "U5": "R5", "U6": "R8", "R2": "D6", "R5": "D5", "R8": "D4", "D6": "L8", "D5": "L5", "D4": "L2", "L8": "U4", "L5": "U5", "L2": "U6", "B3": "B1", "B6": "B2", "B9": "B3", "B2": "B4", "B8": "B6", "B1": "B7", "B4": "B8", "B7": "B9", "L1": "U3", "L4": "U2", "L7": "U1", "D9": "L1", "D8": "L4", "D7": "L7", "R9": "D9", "R6": "D8", "R3": "D7", "U3": "R9", "U2": "R6", "U1": "R3"}
    }
}

config = {}

def load_config():
    global config
    os.chdir(os.path.dirname(__file__))
    if not os.path.isfile("config.json"):
        with open("config.json", "w") as f:
            json.dump(DEFAULT_CONFIG, f)
        raise FileNotFoundError("An empty configuration file has been created. Please fill it out before continuing.")
    with open("config.json", "r") as f:
        config = json.load(f)
    return config





class Face:
    def __init__(self, colors: list[str], moves: str) -> None:
        assert len(colors) == 9
        self.colors = colors
        self.moves = moves
    
    def __repr__(self) -> str:
        return "|".join(self.colors) + " " + self.moves

class Cube:
    def __init__(self, colors: dict[str, str] | None = None, moves: list[str] | None = None) -> None:
        assert colors and len(colors) == 54 # TODO: 54 hardcoded
        self.colors = colors
        self.moves = moves or []

    @staticmethod
    def from_mapping(face_to_color: dict[str, str]):
        colors = {
            face + str(pos): color
            for face, color in face_to_color.items()
            for pos in range(1, 10)
        }
        return Cube(colors)

    def get(self, position):
        return self.colors[position]

    def set(self, position, color):
        self.colors[position] = color

    def apply(self, rotation):
        face, direction = rotation[0], (0 if len(rotation) == 1 else "2'".index(rotation[1])) + 1
        copy = Cube(self.colors.copy(), self.moves + [rotation])

        for _ in range(direction):
            for old_pos, new_pos in config["moves"][face].items():
                copy.set(new_pos, self.get(old_pos))
        
        return copy
    
    def copy(self, next_rotation = None):
        if next_rotation is None:
            return Cube(self.colors.copy(), self.moves.copy())
        return Cube(self.colors.copy(), self.moves.copy() + [next_rotation])
    
    def __hash__(self) -> int:
        return hash("".join(color.value for color in self.colors))
    
    def __repr__(self) -> str:
        return " ".join(str(move) for move in self.moves) + "\n" + "\n".join(
            "".join(
                ' ' if face == ' ' else self.get(face + position)[0].upper()
                for face in faces
                for position in positions
            )
            for faces in [" U  ", "LFRB", " D  "]
            for positions in ["123", "456", "789"]
        )

def format_coord(x: int, y: int) -> str:
    # number = x + 1
    number = y + 1 # TEMP: Team 3
    text = ""
    while number > 0:
        remainder = (number - 1) % 26
        text = chr(65 + remainder) + text
        number = (number - 1) // 26
    # return f"{text}{y + 1}"
    return f"{text}{x + 1}"

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

    # TODO: Make requests a bit better looking than just a JSON file (or load default from file and modify)
    requests = [
        ## Fresco
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
                "rows": [{"values": [{"userEnteredFormat": {
                    "backgroundColor": config["colors"][color],
                    "textFormat": {"foregroundColor": config["colors"][color]}
                }}]}],
                "fields": "*"
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
    
    # Set the coordinates on the fresco
    fresco_rows_text = []
    for i in range(len(moves)):
        line = []
        for j in range(len(moves[i])):
            for _ in range(3):
                # line.append(format_coord(j, i))
                line.append(f"{format_coord(j, i)} - {j // 12 + 1}.{11 - i // 3}.{(j % 12) // 4 + 1}") # TEMP: Team 3
        for _ in range(3):
            fresco_rows_text.append(line)

    # Set the instructions
    i = 0
    moves_rows_text = [("Coords", "Status", "Front", "Up", "Moves")]
    for y, row in enumerate(reversed(moves)):
        for x, move in enumerate(row):
            i += 1
            
            cube = Cube.from_mapping(config["default_cube"])
            m = move.moves
            # TODO: Apply x' rotation on cube AND moves so that the result is on the front and not on top
            # Skip full cube rotation
            if m and m[0].lower() in "xyz":
                rotation = m.split(' ')[0]
                m = ' '.join(m.split(' ')[1:])
                cube = cube.apply(rotation)
            # TODO: Apply z rotation to have no U turns for the robot

            # Get the colors
            front = cube.colors["F5"]
            up = cube.colors["U5"]
            front_rgb = config["colors"][front]
            up_rgb = config["colors"][up]
            if not m:
                front = ""
                front_rgb = {"red": 0.5, "green": 0.5, "blue": 0.5}

            # Write content & colors
            moves_rows_text.append((format_coord(x, len(moves) - 1 - y), "TODO", front, up, m))
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
            if 'U' in m:
                # Impossible move for the robot
                requests.append({
                    "updateCells": {
                        "rows": [
                            {"values": [
                                {"userEnteredFormat": {"backgroundColor": {
                                    "red": 1,
                                    "green": 0,
                                    "blue": 0
                                }}}
                            ]}
                        ],
                        "fields": '*',
                        "range": {
                            "sheetId": config["moves_id"],
                            "startRowIndex": i,
                            "endRowIndex": i + 1,
                            "startColumnIndex": 4,
                            "endColumnIndex": 5
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
            range=sheets_names_by_id[config["fresco_id"]] + "!1:" + str(len(fresco_rows_text)),
            valueInputOption="USER_ENTERED",
            body={"values": fresco_rows_text}
        ).execute()
        sheets.values().update(
            spreadsheetId=config["spreadsheet_id"],
            range=sheets_names_by_id[config["moves_id"]] + "!A:E",
            valueInputOption="USER_ENTERED",
            body={"values": moves_rows_text}
        ).execute()

    except HttpError as err:
        print(err)



def main():
    load_config()
    soup = convert_image(config["image_path"])
    moves = extract_moves(soup)
    write_to_spreadsheets(moves)

if __name__ == "__main__":
    main()
