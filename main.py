import os
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from auth import *
from tasklist import *


def main():
    credentials = get_credentials()
    service = build("tasks", "v1", credentials=credentials)
    list_tasklists(service)


main()
