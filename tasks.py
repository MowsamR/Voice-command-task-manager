import datetime


class Task:
    # DOCS: https://developers.google.com/tasks/reference/rest/v1/tasks

    def __init__(self, id: str, title: str,
                 due_date: datetime = None,
                 notes: str = "Add Description", status: str = "needsAction") -> None:

        self.id = id
        self.title = title
        self.date_updated: datetime = datetime.datetime.now().isoformat()
        self.due_date = due_date
        self.notes = notes
        self.status = status
        self.valid_status = {"needsAction", "completed"}

        self.validate()  # Validate after initializing the object

    def validate(self):
        """
        Validation method to check whether the inputs are valid before creating an object
        """
        if not isinstance(self.title, str) or not self.title.strip():
            raise ValueError("Task title cannot be empty.")
        if self.due_date is not None and not isinstance(self.due_date, datetime.datetime):
            raise ValueError(
                "Due date must be a valid datetime object or None.")
        if self.status not in self.valid_status:
            raise ValueError(
                f"Status must have 'needsAction' or 'completed' field.")

    def convert_to_dict(self):
        """
        Convert into Dictionary for API interaction
        """
        if isinstance(self.due_date, datetime.datetime):
            self.due_date = self.due_date.isoformat()

        task_dict = {
            "id": self.id,
            "title": self.title,
            "notes": self.notes,
            "due": self.due_date,
            "status": self.status
        }

        return task_dict

    def mark_complete(self):
        """
        When user completes tasks, changes the state of status to complete.
        """
        status = "completed"
        date_updated = datetime.datetime.now()
        return status

    def change_due_date(self, new_due_date: datetime):
        if (new_due_date < datetime.datetime.now()):
            raise ValueError("Due date cannot be before today.")
        self.due_date = new_due_date
