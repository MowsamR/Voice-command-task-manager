from tasks import Task
from datetime import datetime
from print_string import PrintStrings as ps


class TaskManager:
    def __init__(self, service) -> None:
        self.task_service = service

    def create_task(self, task_list_id, title, notes=None, due_date=None):
        """Create a new task in a specific task list."""
        # TO_DO:CHANGE THE Task_list_id and set it to task ID
        new_task = Task(None, title, notes,
                        due_date)  # Task ID will be set after API call
        response = self.task_service.tasks().insert(
            task_list_id, new_task.to_dict()).execute()

        new_task.id = response["id"]

        return new_task

    def get_task(self, task_list_id, task_id):
        """Fetch a single task by ID."""
        response = self.google_tasks_client.get_task(task_list_id, task_id)
        return Task(response['id'], response['title'], response.get('notes'), response.get('due'))

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

    def task_api_call(self):
        task = self.get_details(self.get_task_action())
        return task
    # def display_task(self, task_id):

    #     try:
    #         # Retrieve all tasks from the specified task list
    #         result = self.service.tasks().list(tasklist=tasklist_id).execute()
    #         tasks = result.get('items', [])

    #         if not tasks:
    #             print("No tasks found.")
    #         else:
    #             print(DIVIDER)
    #             print("Tasks:")
    #             print(DIVIDER)

    #             for task in tasks:
    #                 print(f"Task ID: {task['id']}, Title: {task['title']}")

    #     except Exception as e:
    #         print(f"An error occurred: {e}")
