def list_tasklists(service):
    """
    Prints out all the task lists title and their IDs to the console.
    """
    results = service.tasklists().list().execute()
    tasklists = results.get('items', [])

    if not tasklists:
        print('No task lists found.')
    else:
        print('Task lists:')
        for tasklist in tasklists:
            print(f"- {tasklist['title']} (ID: {tasklist['id']})")
