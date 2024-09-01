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
            self.all_task_lists[new_tl.tl_id] = new_tl

            print(ps.divider)
            print("Successfully created task list.")
            print(ps.divider + ps.newline)

        except HttpError as http_err:
            self.handle_http_error(http_err)

    def get_tasklist(self, tl_id):
        """Get TaskList object based on task list ID."""

        if tl_id in self.all_task_lists:
            print(f"Task list: {self.all_task_lists[tl_id].tl_title}")
            return self.all_task_lists[tl_id]

        else:
            print("Task list ID doesn't exist.")

    def refresh_tasklists(self):
        """
        1. Fetches all the task lists using Get API call
        2. Stores this in all_task_lists() dict
        """
        try:
            tasklist_results = self.task_list_service.tasklists().list().execute()
            tasklists_items = tasklist_results.get('items', [])

            missing_tasklists = [
                task for task in tasklists_items if task['id'] not in self.all_task_lists]

            for tasklist in missing_tasklists:
                tasklist_ID = tasklist["id"]
                tasklist_title = tasklist["title"]
                tl = TaskList(tasklist_title, tasklist_ID)
                self.all_task_lists[tasklist["id"]] = tl

        except HttpError as http_err:
            self.handle_http_error(http_err)

    def show_tasklists(self, refresh=False):
        """
        Show all task lists. If refresh is True, update the list with the latest task lists from the API.
        """
        if refresh or not self.all_task_lists:
            self.refresh_tasklists()
        self.print_tasklists()

    def print_tasklists(self):
        print(ps.divider)
        print("***LIST ALL TASK LIST***")
        print(ps.divider + ps.newline)
        if not self.all_task_lists:
            print("There are 0 tasklists to view.")
        else:
            counter = 1
            for tasklist in self.all_task_lists.values():
                print(f"{counter}. {tasklist.tl_title} --- {tasklist.tl_id}")
                counter += 1
            print(ps.newline + ps.divider + ps.newline)

    def handle_http_error(self, http_err):
        error_content = http_err.content.decode(
            "utf-8") if http_err.content else "No content"
        print(
            f"HttpError occurred: Status code: {http_err.resp.status}, Reason: {http_err.resp.reason}")
        print(f"Error details: {error_content}")

    def task_list_api_call(self):
        # Load the first time so when the script gets called it's filled with existing tasklists inside the dict
        load = self.get_all_tasklist()
        task_list = self.get_details(self.get_task_list_action())
        return task_list
