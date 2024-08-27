from googleapiclient.errors import HttpError
from tasks import *
from tasklist import *
from print_string import PrintStrings as ps

"""
Interface that manager the interaction between Task class and TaskList class
"""


class TaskListManager:
    def __init__(self, service) -> None:
        self.all_task_lists = {}  # {key: ID, value: TaskList }
        self.task_list_service = service

    def create_tasklist(self, tl_title):
        """Create a new Task List."""
        try:
            tl_body = {'title': tl_title}
            response = self.task_list_service.tasklist.insert(
                body=tl_body).execute()

            new_tl = TaskList(response["id"], response["title"])
            self.all_task_lists[new_tl] = new_tl

            print(ps.divider)
            print("Successfully created task list.")
            print(ps.divider + ps.newline)

        except HttpError as http_err:
            # Capture and print detailed HTTP error information
            error_content = http_err.content.decode(
                "utf-8") if http_err.content else "No content"

            print(
                f"HttpError occurred: Status code: {http_err.resp.status}, Reason: {http_err.resp.reason}")

            print(f"Error details: {error_content}")

    def get_tasklist(self, tasklist_ID):
        """Get TaskList object based on task list ID."""
        pass

    def get_all_tasklist(self):
        """
        1. Fetches all the task lists using Get API call
        2. Stores this in all_task_lists() dict
        """
        try:
            results = self.task_list_service.tasklists().list().execute()
            tasklists_items = results.get('items', [])
            self.all_task_lists.clear()

            for tasklist in tasklists_items:
                tasklist_ID = tasklist["id"]
                tasklist_title = tasklist["title"]
                tl = TaskList(tasklist_ID, tasklist_title)
                self.all_task_lists[tasklist["id"]] = tl

        except HttpError as http_err:
            # Capture and print detailed HTTP error information
            error_content = http_err.content.decode(
                "utf-8") if http_err.content else "No content"

            print(
                f"HttpError occurred: Status code: {http_err.resp.status}, Reason: {http_err.resp.reason}")

            print(f"Error details: {error_content}")

    def print_tasklists(self):
        print(ps.divider + ps.newline)
        counter = 1
        for tasklist in self.all_task_lists.values():
            print(f"{counter}. {tasklist.title} --- {tasklist.ID}")
            counter += 1
        print(ps.newline + ps.divider + ps.newline)

    # CHANGE this to match Task list details not task details that's copied from there.
    def get_details(self, action: str):
        """
        Get the details required depending on the specific action called.
        """
        match action:
            case "c":
                tl_title = input("Enter task list title: ")
                return self.create_tasklist(tl_title)

            case "g":
                task_list_id = input("Enter Task List ID: ")
                task_id = input("Enter Task ID: ")
                return self.get_tasklist(task_list_id, task_id)

            case "d":
                # delete
                # if success return print("successfully deleted task")
                pass

    def get_task_list_action(self):
        '''
        Get the action (Task List: Create, Get, Delete)
        '''
        print(ps.divider)
        print("***GET TASK LIST ACTION***")
        print(ps.divider + ps.newline)

        print(
            f"1. Create task list (type 'c'){ps.newline}2. Get task list (type 'g'){ps.newline}3. Delete task list(type 'd'){ps.newline*2}* Enter your action: ")
        print(ps.newline + ps.divider)

        user_action = input().strip()

        if user_action in ['c', 'g', 'd']:
            return user_action
        else:
            print("Invalid action. Please try again.")
            return self.get_task_list_action()

    def task_list_api_call(self):
        task_list = self.get_details(self.get_task_list_action())
        return task_list
