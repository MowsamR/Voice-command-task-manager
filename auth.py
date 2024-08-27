import os
import os.path
import json
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

    # Check if the token file exists and try to load it
    if os.path.exists(token_path):
        try:
            credentials = Credentials.from_authorized_user_file(
                token_path, SCOPES)
            print("Token exists.")
        except (ValueError, json.JSONDecodeError) as e:
            print(f"Corrupted token file, deleting it: {e}")
            os.remove(token_path)
            credentials = None

    # If the token is invalid or missing, handle re-authentication
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            try:
                credentials.refresh(Request())
            except Exception as e:
                print(f"Error refreshing token: {e}")
                # Delete the expired token and force re-authentication
                if os.path.exists(token_path):
                    os.remove(token_path)
                credentials = None  # Reset credentials to trigger new login

        if not credentials:
            # Trigger new authentication flow
            flow = InstalledAppFlow.from_client_secrets_file(
                client_secret_path, SCOPES)
            credentials = flow.run_local_server(port=0)
            # Save the new credentials
            with open(token_path, "w") as token:
                token.write(credentials.to_json())

    return credentials
