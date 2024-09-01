from tasks import *
from tasklist import *
from print_string import PrintStrings as ps
from task_list_manager import *
from task_manager import *


class InputManager:
    def __init__(self, task_list_manager: TaskListManager, task_manager: TaskManager):
        self.task_list_manager = task_list_manager
        self.task_manager = task_manager
        self.fetch_data_count = 0

    def start(self):
        """
        Main loop that runs until the user types 'quit'.
        """

        while True:
            print(ps.divider)
            print("***MAIN MENU***")
            print(ps.divider + ps.newline)
            print("What would you like to do? (type 'quit' to exit)")
            print("1. Manage Task Lists")
            print("2. Manage Tasks")
            print(ps.divider)

            action = input(
                "Enter your choice (1/2) or type 'quit' to exit: ").strip()

            if action.lower() == 'quit':
                print("Exiting the program. Goodbye!")
                break
            elif action == '1':
                self.manage_task_lists()
            elif action == '2':
                self.manage_tasks()
            else:
                print("Invalid choice. Please try again.")

    def manage_task_lists(self):
        """
        Handles all interactions related to task lists.
        """
        print(ps.divider)
        print("***Task List Management***")
        print(ps.divider + ps.newline)
        print("1. Create a new task list")
        print("2. View all task lists")
        print("3. Show all tasks in a task list ")
        print("4. Delete a task list")
        print(ps.divider)

        action = input(
            "Enter your choice (1/2/3) or type 'quit' to exit: ").strip()

        if action.lower() == 'quit':
            return
        elif action == '1':
            tl_title = input("Enter task list title: ").strip()
            self.task_list_manager.create_tasklist(tl_title)
            print(ps.newline)

        elif action == '2':
            self.task_list_manager.show_tasklists()
            print(ps.newline)

        elif action == '3':
            self.task_list_manager.show_tasklists()

            tasklist_id = input("Enter the Tasklist ID: ")
            chosen_tasklist = self.task_list_manager.get_tasklist(
                tasklist_id)

            self.task_manager.show_tasks_in_tasklist(chosen_tasklist)

        elif action == '4':
            # self.manager.print_tasklists()
            # tl_id = input("Enter Task List ID to delete: ").strip()
            # self.manager.delete_tasklist(tl_id)
            pass
        else:
            print("Invalid choice. Please try again.")
            self.manage_task_lists()

    def manage_tasks(self):
        """
        Handles all interactions related to tasks.
        """
        print(ps.divider)
        print("***Task Management***")
        print(ps.divider + ps.newline)
        print("1. Create a Task")
        print("2. View Tasks in a Task List")
        print("3. Delete a Task")
        print(ps.divider)

        action = input(
            "Enter your choice (1/2/3) or type 'quit' to exit: ").strip()

        if action.lower() == 'quit':
            return
        elif action == '1':
            self.task_list_manager.print_tasklists()

            task_list_id = input("Enter task list ID: ").strip()
            title = input("Enter task title: ").strip()
            notes = input("Enter Description (Optional): ").strip()

            input_date = input("Enter the date in yyyy/mm/dd format: ")
            date_object = datetime.strptime(input_date, "%Y/%m/%d")
            rfc3339_format = date_object.isoformat()

            self.create_task(task_list_id, title, notes, rfc3339_format)

        elif action == '2':
            self.task_list_manager.print_tasklists()
            tl_id = input("Enter Task List ID to view tasks: ").strip()
            self.view_tasks(tl_id)

        elif action == '3':
            self.task_list_manager.print_tasklists()
            tl_id = input("Enter Task List ID: ").strip()
            self.view_tasks(tl_id)
            task_id = input("Enter Task ID to delete: ").strip()
            self.delete_task(tl_id, task_id)
        else:
            print("Invalid choice. Please try again.")
            self.manage_tasks()

    def create_task(self, tl_id, task_title):
        task = Task(task_title)
        task_list = self.task_list_manager.get_tasklist(tl_id)
        if task_list:
            task_list.add_task(task)
            print("Task created successfully.")

    def view_tasks(self, tl_id):
        task_list = self.task_list_manager.get_tasklist(tl_id)
        if task_list:
            task_list.print_tasks()

    def delete_task(self, tl_id, task_id):
        task_list = self.task_list_manager.get_tasklist(tl_id)
        if task_list:
            task_list.delete_task(task_id)
            print("Task deleted successfully.")
