from tasks import Task


class TaskList:
    def __init__(self, tl_title, tl_id=None):
        self.tl_id = tl_id
        self.tl_title = tl_title
        self.all_tasks = {}  # (key: task_id , value: Task())

    def add_task(self, task: Task):
        if not isinstance(task, Task):
            raise TypeError("The parameter must be a Task instance.")
        self.all_tasks[task.id] = task

    def remove_task(self, task: Task):
        if not isinstance(task, Task):
            raise TypeError("The parameter must be a Task instance.")
        if task.id in self.all_tasks:
            del self.all_tasks[task.id]
        else:
            raise KeyError(f"Task with ID {task.id} not found.")

    def list_all_tasks(self):
        '''
        Print all tasks under this task list.
        '''
        pass
