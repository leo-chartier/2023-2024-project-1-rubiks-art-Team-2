PATH = "../Images/Final_reworked-website_colors.png"
HTML_PARSER = "html.parser"

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

SPREADSHEET_ID = "TO BE HIDDEN"
FRESCO_ID = 0
CELL_SIZE = 5
COLORS = {
    "white":  {"red": 1, "green": 1,    "blue": 1},
    "yellow": {"red": 1, "green": 1,    "blue": 0},
    "blue":   {"red": 0, "green": 0.5,  "blue": 1},
    "green":  {"red": 0, "green": 0.75, "blue": 0},
    "red":    {"red": 1, "green": 0,    "blue": 0},
    "orange": {"red": 1, "green": 0.5,  "blue": 0},
}



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
    from typing import Callable
except ImportError:
    os.system("python3 -m pip install --upgrade beautifulsoup4 selenium Pillow google-api-python-client google-auth-httplib2 google-auth-oauthlib")
    print("Dependencies have been installed. Please execute the program again.")
    exit()





class Face:
    def __init__(self, colors: list[str], moves: str) -> None:
        assert len(colors) == 9
        self.colors = colors
        self.moves = moves
    
    def __repr__(self) -> str:
        return "|".join(self.colors) + " " + self.moves

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
    soup = BeautifulSoup(driver.page_source, features=HTML_PARSER)
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
    
    for row in reversed(rows):
        moves.append([])
        for column in row:
            moves[-1].append(Face(
                [cubelet["style"].split(" ")[1][:-1] for cubelet in column.contents[1].find_all(class_="cube-square")],
                column.contents[2].text
            ))

    assert len(moves) % 3 == 0
    assert all(len(row) % 3 == 0 for row in moves)
    assert len(set(len(row) for row in moves)) == 1

    return moves

def write_to_spreadsheets(moves: list[list[Face]]):
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request()) # If this fails, delete token.json
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('sheets', 'v4', credentials=creds)

        # Call the Sheets API
        sheets = service.spreadsheets()
        # sheet.values().clear(SPREADSHEET_ID, "")
        body = {"requests": [
            {"updateCells": {
                "range": {"sheetId": FRESCO_ID},
                "fields": "effectiveFormat"
            }},
            {"updateSheetProperties": {
                "properties": {
                    "gridProperties": {"rowCount": len(moves) * 3, "columnCount": len(moves[0]) * 3},
                    "sheetId": FRESCO_ID
                },
                "fields": "gridProperties"
            }},
            {"updateDimensionProperties": {
                "range": {"sheetId": FRESCO_ID, "dimension": "COLUMNS"},
                "properties": {"pixelSize": CELL_SIZE},
                "fields": "pixelSize"
            }},
            {"updateDimensionProperties": {
                "range": {"sheetId": FRESCO_ID, "dimension": "ROWS"},
                "properties": {"pixelSize": CELL_SIZE},
                "fields": "pixelSize"
            }}
        ]}
        for i in range(len(moves) * 3):
            row = moves[i // 3]
            for j in range(len(row) * 3):
                face = row[j // 3]
                color = face.colors[3 * (i % 3) + (j % 3)]
                body["requests"].append({"updateCells": {
                    "range": {
                        "sheetId": FRESCO_ID,
                        "startRowIndex": i,
                        "endRowIndex": i + 1,
                        "startColumnIndex": j,
                        "endColumnIndex": j + 1
                    },
                    "rows": [{"values": [{"userEnteredFormat": {"backgroundColor": COLORS[color]}}]}],
                    "fields": "userEnteredFormat.backgroundColor"
                }})
        print(body["requests"][-1])
        sheets.batchUpdate(spreadsheetId=SPREADSHEET_ID, body=body).execute()

    except HttpError as err:
        print(err)



def main():
    os.chdir(os.path.dirname(__file__))
    soup = convert_image(PATH)
    moves = extract_moves(soup)
    write_to_spreadsheets(moves)

if __name__ == "__main__":
    main()
