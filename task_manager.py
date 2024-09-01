from tasks import Task
from datetime import datetime
from print_string import PrintStrings as ps
from googleapiclient.errors import HttpError
from tasklist import TaskList


class TaskManager:
    def __init__(self, service) -> None:
        self.task_service = service

    def create_task(self, task_list_id, title, notes=None, due_date=None):
        """Create a new task in a specific task list."""
        # TO_DO:CHANGE THE Task_list_id and set it to task ID
        try:
            new_task = Task(None, title, notes,
                            due_date)  # Task ID will be set after API call
            response = self.task_service.tasks().insert(
                task_list_id, new_task.to_dict()).execute()

            new_task.id = response["id"]
        except HttpError as http_err:
            self.handle_http_error(http_err)

        return new_task

    def get_task(self, task_list_id, task_id):
        """Fetch a single task by ID."""
        try:
            response = self.google_tasks_client.get_task(task_list_id, task_id)
            task = Task(response['id'], response['title'],
                        response.get('notes'), response.get('due'))
        except HttpError as http_err:
            self.handle_http_error(http_err)

        return

    def get_details(self, action: str):
        """
        Get the details required depending on the specific action called.
        """
        match action:
            case "c":
                task_list_id = input("Enter task list ID: ")
                title = input("Enter task title: ")
                notes = input("Enter Description (Optional): ")

                input_date = input("Enter the date in yyyy/mm/dd format: ")
                date_object = datetime.strptime(input_date, "%Y/%m/%d")
                rfc3339_format = date_object.isoformat()

                return self.create_task(task_list_id, title, notes, rfc3339_format)

            case "g":
                task_list_id = input("Enter Task List ID: ")
                task_id = input("Enter Task ID: ")
                return self.get_task(task_list_id, task_id)

            case "d":
                # delete
                # if success return print("successfully deleted task")
                pass

    def get_task_action(self):
        '''
        Get the action (Task: Create, Get, Delete)
        '''
        print(ps.divider)
        print("***GET TASK ACTION***")
        print(ps.divider + ps.newline)

        print(
            f"1. Create task (type 'c'){ps.newline}2. Get task (type 'g'){ps.newline}3. Delete task (type 'd'){ps.newline*2}* Enter your action: ")
        print(ps.newline + ps.divider)

        user_action = input().strip()

        if user_action in ['c', 'g', 'd']:
            return user_action
        else:
            print("Invalid action. Please try again.")
            return self.get_task_action()

    def refresh_missing_tasks(self, tasklist: TaskList):
        """
        Shows all the tasks inside a task list
        """

        # Don't want to fetch all tasks for all tasklists
        # Only fetch all tasks when a given tasklist is called, so that what's asked is what's shown only

        # Steps:
        # 1. service.tasks().list().execute() which returns [Tasks]
        # 2. iterate and populate these [Tasks] in TaskList.all_tasks dictionary (key: task_id , value: Task())
        # 3. call TaskList.list_all_tasks() to print all tasks
        try:
            # Fetch all tasks from the API
            response = self.task_service.tasks().list(tasklist=tasklist).execute()
            api_tasks = response.get('items', [])

            # Find tasks that are not in the dictionary (missing tasks)
            missing_tasks = [
                task for task in api_tasks if task['id'] not in tasklist.all_tasks]

            # Add missing tasks to the all_tasks dictionary
            for task_data in missing_tasks:
                task_id = task_data['id']
                task_title = task_data['title']
                # Assuming Task class takes id and title as parameters
                task = Task(task_id, task_title)
                tasklist.all_tasks[task_id] = task

        except HttpError as http_err:
            print(f"Failed to retrieve tasks: {http_err}")

    def show_tasks_in_tasklist(self, refresh, tasklist: TaskList):
        """
        Refresh/Fetch when tasks are updated or deleted for performance
        """
        if refresh or not tasklist.all_tasks:
            self.refresh_missing_tasks(tasklist)

        tasklist.list_all_tasks()

    def handle_http_error(self, http_err):
        error_content = http_err.content.decode(
            "utf-8") if http_err.content else "No content"
        print(
            f"HttpError occurred: Status code: {http_err.resp.status}, Reason: {http_err.resp.reason}")
        print(f"Error details: {error_content}")

    def task_api_call(self):
        task = self.get_details(self.get_task_action())
        return task
