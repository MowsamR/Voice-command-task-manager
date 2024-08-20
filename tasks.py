import datetime


class Task:
    # DOCS: https://developers.google.com/tasks/reference/rest/v1/tasks

    def __init__(self, id: str, title: str,
                 date_updated: datetime, due_date: datetime = None,
                 notes: str = "Add Description", status: str = "needsAction") -> None:

        self.id = id
        self.title = title
        self.date_updated = date_updated
        self.due_date = due_date
        self.notes = notes
        self.status = status

    def convert_to_dict(self):
        """
        Convert into Dictionary for API interaction
        """
        task_dict = {
            "id": self.id,
            "title": self.title,
            "updated": self.date_updated,
            "notes": self.notes,
            "due": self.due_date,
            "status": self.status
        }

        return task_dict
