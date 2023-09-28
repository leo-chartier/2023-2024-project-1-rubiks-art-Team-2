from __future__ import print_function

from PIL import Image

import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError





PATH = "../image.png"
img = Image.open(PATH)

# # Create a version of the image with black spacing
# spaced = Image.new("RGB", (int(img.width / 3 * 4) + 1, int(img.height / 3 * 4) + 1), (0, 0, 0))
# for x in range(img.width // 3):
#     for y in range(img.height // 3):
#         spaced.paste(img.crop((3*x, 3*y, 3*x+3, 3*y+3)), (4*x+1, 4*y+1))
# spaced.show()





# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = ''
SAMPLE_RANGE_NAME = 'Main!A2:E'



creds = None
# The file token.json stores the user's access and refresh tokens, and is
# created automatically when the authorization flow completes for the first
# time.
if os.path.exists('token.json'):
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
# If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open('token.json', 'w') as token:
        token.write(creds.to_json())

try:
    pass # TODO

except HttpError as err:
    print(err)
