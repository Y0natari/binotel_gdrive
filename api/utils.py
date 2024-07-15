import httpx
import io
import logging
from datetime import datetime
import pytz
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload

# Changable Constants
BINOTEL_API_KEY = "<YOUR_BINOTEL_API_KEY_HERE>" 
BINOTEL_API_SECRET = "<YOUR_BINOTEL_API_SECRET_HERE>"
FOLDER_ID = None # Set up this field if necessary
SERVICE_ACCOUNT_FILE = '<google_key_name>.json' # Set up the name of .json secret key here
TIMEZONE = 'Europe/Kyiv'  # Change timezone if needed

# Constants
BINOTEL_API_URL = "https://api.binotel.com/api/4.0/stats/call-record.json"
SCOPES = ['https://www.googleapis.com/auth/drive.file']

# Setup Google Drive API credentials
credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
drive_service = build('drive', 'v3', credentials=credentials)

# fetch the link on a record
async def fetch_call_record(general_call_id: int) -> str:
    async with httpx.AsyncClient() as client:
        post_data = {
            "key": BINOTEL_API_KEY,
            "secret": BINOTEL_API_SECRET,
            "generalCallID": general_call_id
        }

        response = await client.post(BINOTEL_API_URL, json=post_data, headers={'Content-Type': 'application/json'})

        if response.status_code == 200:
            response_data = response.json()
            if response_data.get("status") == "success":
                return response_data.get("url")
            else:
                logging.info(f"REST API error {response_data['code']}: {response_data['message']}")
        else:
            logging.info(f"Server error: {response.text}")
    return None

# download to IO Buffer
async def download_to_buffer(url: str) -> io.BytesIO:
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code == 200:
            return io.BytesIO(response.content)
        else:
            raise Exception(f"Failed to download file: {response.status_code} - {response.text}")

# upload a file on Google Drive
def upload_to_google_drive(file_buffer: io.BytesIO, file_name: str, folder_id: str = FOLDER_ID):
    media = MediaIoBaseUpload(file_buffer, mimetype='audio/mpeg')
    file_metadata = {
        'name': file_name,
        'mimeType': 'audio/mpeg',
        'parents': [folder_id]
    }

    file = drive_service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id'
    ).execute()
    logging.info(f"File uploaded successfully. File ID: {file.get('id')}")

# Generate a name
def generate_filename() -> str:
    tz = pytz.timezone(TIMEZONE)
    utc_now = datetime.now(pytz.utc)
    tz_now = utc_now.astimezone(tz)
    return tz_now.strftime('%H:%M:%S %d/%m/%y')
