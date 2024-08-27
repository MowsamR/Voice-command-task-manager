import os
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from auth import *
from tasklist import *
from task_manager import *
from task_list_manager import *


def main():

    credentials = get_credentials()
    task_service = build("tasks", "v1", credentials=credentials)
    task_list_service = build("tasks", "v1", credentials=credentials)

    task_manager = TaskManager(task_service)
    task_list_manager = TaskListManager(task_list_service)

    # try:

    #     task_manager = TaskManager(task_service)
    # except Exception as e:
    #     print(f"An error occurred: {e}")

    # print("=============================\n")

    # task_manager.task_api_call()
    task_list_manager.get_all_tasklist()
    task_list_manager.print_tasklists()

    # task_manager.create_task()


main()
