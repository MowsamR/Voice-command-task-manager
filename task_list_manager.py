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
            response = self.task_list_service.tasklists().insert(
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

    def get_tasklist(self, tl_id):
        """Get TaskList object based on task list ID."""

        if tl_id in self.all_task_lists:
            print(f"Task list: {self.all_task_lists[tl_id].tl_title}")
            return self.all_task_lists[tl_id]

        else:
            print("Task list ID doesn't exist.")

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
                tl = TaskList(tasklist_title, tasklist_ID)
                self.all_task_lists[tasklist["id"]] = tl

        except HttpError as http_err:
            # Capture and print detailed HTTP error information
            error_content = http_err.content.decode(
                "utf-8") if http_err.content else "No content"

            print(
                f"HttpError occurred: Status code: {http_err.resp.status}, Reason: {http_err.resp.reason}")

            print(f"Error details: {error_content}")

    def print_tasklists(self):
        print(ps.divider)
        print("***LIST ALL TASK LIST***")
        print(ps.divider + ps.newline)
        counter = 1
        for tasklist in self.all_task_lists.values():
            print(f"{counter}. {tasklist.tl_title} --- {tasklist.tl_id}")
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
                self.print_tasklists()
                task_list_id = input("Enter Task List ID: ")
                return self.get_tasklist(task_list_id)

            case "d":
                # delete
                # if success return print("successfully deleted task")
                pass

            case "p":
                self.print_tasklists()

    def get_task_list_action(self):
        '''
        Get the action (Task List: Create, Get, Delete)
        '''
        print(ps.divider)
        print("***GET TASK LIST ACTION***")
        print(ps.divider + ps.newline)

        print(
            f"1. Create task list (type 'c'){ps.newline}2. Get task list (type 'g'){ps.newline}3. Delete task list(type 'd'){ps.newline}4. Print all task lists(type 'p'){ps.newline*2}* Enter your action: ")
        print(ps.newline + ps.divider)

        user_action = input().strip()

        if user_action in ['c', 'g', 'd', 'p']:
            return user_action
        else:
            print("Invalid action. Please try again.")
            return self.get_task_list_action()

    def task_list_api_call(self):
        # Load the first time so when the script gets called it's filled with existing tasklists inside the dict
        load = self.get_all_tasklist()
        task_list = self.get_details(self.get_task_list_action())
        return task_list
