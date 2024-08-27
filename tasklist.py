from tasks import Task


class TaskList:
    def __init__(self, tl_title, tl_id=None):
        self.tl_id = tl_id
        self.tl_title = tl_title
        self.tasks = {}  # (key: task_id )

    def add_task(self, task: Task):
        return

    def add_task(self, task: Task):
        return self.tasks.remove(task)

    def list_all_tasks(self):
        '''
        Print all tasks under this task list.
        '''
        pass

    def convert_to_dict(self):
        """
        Convert into Dictionary for API interaction
        """
        tl_dict = {
            "id": self.tl_id,
            "title": self.tl_title,
        }

        return tl_dict
