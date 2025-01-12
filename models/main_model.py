import sqlite3
from typing import List, Dict
from datetime import datetime

today = str(datetime.today().date().strftime('%d/%m/%Y'))

class TaskModel:
    def __init__(self, db_path: str = "todo_app.db"):
        """
        Initialize the TaskModel and connect to the SQLite database.

        :param db_path: Path to the SQLite database file.
        """
        self.db_path = db_path
        self.connection = sqlite3.connect(self.db_path)
        self._create_table()

    def _create_table(self):
        """
        Create the tasks table if it doesn't exist.
        """
        cursor = self.connection.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY AUTOINCREMENT,title TEXT NOT NULL,
        description TEXT, completed BOOLEAN DEFAULT 0, important BOOLEAN DEFAULT 0, due_date TEXT, created_date TEXT)
        """)
        self.connection.commit()

    def add_task(self, title: str, description: str = "", due_date: str = None, created_date: str = today) -> int:
        """
        Add a new task to the database.

        :param title: Title of the task.
        :param description: Description of the task (optional).
        :param due_date: Due date for the task in YYYY-MM-DD format (optional).
        :return: ID of the newly created task.
        """
        cursor = self.connection.cursor()
        cursor.execute("""
        INSERT INTO tasks (title, description, completed, important, due_date, created_date)
        VALUES (?, ?, 0, 0, ?, ?)
        """, (title, description, due_date, created_date))
        self.connection.commit()
        return cursor.lastrowid

    def get_all_tasks(self) -> List[Dict]:
        """
        Retrieve all tasks from the database.

        :return: List of tasks, each represented as a dictionary.
        """
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM tasks")
        rows = cursor.fetchall()
        tasks = [
            {"id": row[0], "title": row[1], "description": row[2], "completed": bool(row[3]), "important": bool(row[4]),
             "due_date": row[5], "created_date": row[6]}
            for row in rows
        ]
        return tasks

    def get_a_task(self, task_id: int) -> Dict:
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
        row = cursor.fetchone()
        if row is None:
            return None  # No task found with the given ID

        # Convert the row into a dictionary
        task = {
            "id": row[0],
            "title": row[1],
            "description": row[2],
            "completed": bool(row[3]),
            "important": bool(row[4]),
            "due_date": row[5],
            "created_date": row[6],
        }
        return task

    def update_task(self, task_id: int, title: str = None, description: str = None, completed: bool = None, important: bool = None,
                    due_date: str = None, created_date: str = None):
        """
        Update an existing task in the database.

        :param task_id: ID of the task to update.
        :param title: New title for the task (optional).
        :param description: New description for the task (optional).
        :param completed: New completion status for the task (optional).
        :param due_date: New due date for the task (optional).
        """
        updates = []
        params = []
        if title is not None:
            updates.append("title = ?")
            params.append(title)
        if description is not None:
            updates.append("description = ?")
            params.append(description)
        if completed is not None:
            updates.append("completed = ?")
            params.append(int(completed))  # SQLite uses 0/1 for BOOLEAN
        if due_date is not None:
            updates.append("due_date = ?")
            params.append(due_date)
        if created_date is not None:
            updates.append("created_date = ?")
            params.append(created_date)
        if important is not None:
            updates.append("important = ?")
            params.append(important)

        if updates:
            cursor = self.connection.cursor()
            query = f"UPDATE tasks SET {', '.join(updates)} WHERE id = ?"
            params.append(task_id)
            cursor.execute(query, params)
            self.connection.commit()

    def delete_task(self, task_id: int):
        """
        Delete a task from the database.

        :param task_id: ID of the task to delete.
        """
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        self.connection.commit()

    def close_connection(self):
        """
        Close the connection to the database.
        """
        self.connection.close()


if __name__ == "__main__":
    # Sample usage
    model = TaskModel()

    # Add a task
    task_id = model.add_task("Buy groceries", "Milk, Bread, Eggs", "2024-01-10")
    print(f"Task added with ID: {task_id}")

    # Get all tasks
    tasks = model.get_all_tasks()
    print("All Tasks:", tasks)

    # Update a task
    model.update_task(task_id, completed=True)
    print("Updated Task:", model.get_all_tasks())

    # Delete a task
    model.delete_task(task_id)
    print("Remaining Tasks:", model.get_all_tasks())

    # Close the connection
    model.close_connection()