import os
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

client_secret_path = os.getenv("GOOGLE_CLIENT_SECRET_PATH")
token_path = os.getenv("GOOGLE_TOKEN_PATH")

SCOPES = ['https://www.googleapis.com/auth/tasks',
          'https://www.googleapis.com/auth/calendar']


def get_credentials():
    credentials = None
    if os.path.exists(token_path):
        # These credentials are required to access API calls
        credentials = Credentials.from_authorized_user_file(
            token_path, SCOPES)
        print("Token exists and is valid.")

    # if credentials is missing or isn't valid:
    if not credentials or not credentials.valid:
        # if the credential that exists has expired, refresh the credentials
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())

        # If it doesn't exist, you need to log in.
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                client_secret_path, SCOPES)
            credentials = flow.run_local_server(port=0)

        # save the credential to token.json so that it can be reused
        with open(token_path, "w") as token:
            token.write(credentials.to_json())

    return credentials
