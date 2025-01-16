from typing import List, Dict
from datetime import date, datetime, timedelta
from context import database as db
from context import localStorage

today = str(datetime.today().date().strftime('%d/%m/%Y'))
tomorrow = (date.today() + timedelta(days=1)).strftime('%d/%m/%Y')

class TaskModel:
    # def __init__(self, db_path: str = "todo_app.db"):
    #     """
    #     Initialize the TaskModel and connect to the SQLite database.

    #     :param db_path: Path to the SQLite database file.
    #     """
    #     self.db_path = db_path
    #     self.connection = sqlite3.connect(self.db_path)
    #     self._create_table()

    # def _create_table(self):
    #     """
    #     Create the tasks table if it doesn't exist.
    #     """
    #     cursor = self.connection.cursor()
    #     cursor.execute("""CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY AUTOINCREMENT,title TEXT NOT NULL,
    #     description TEXT, completed BOOLEAN DEFAULT 0, important BOOLEAN DEFAULT 0, due_date TEXT, created_date TEXT, is_myday BOOLEAN DEFAULT 0, expired_date_myday TEXT DEFAULT '01/01/1970')
    #     """)
    #     self.connection.commit()

    def add_task(self, title: str, description: str = "", due_date: str = '01/01/1970', created_date: str = today,
                 important: bool = False, is_myday: bool = False, expired_date_myday: str = tomorrow) -> int:
        """
        Add a new task to the database.

        :param title: Title of the task.
        :param description: Description of the task (optional).
        :param due_date: Due date for the task in YYYY-MM-DD format (optional).
        :return: ID of the newly created task.
        """
        connection = db.connect_db()
        userID = localStorage.userID
        cursor = connection.execute("""
        INSERT INTO Tasks (UserID, Title, Description, IsCompleted, IsImportant, DueDate, CreatedDate, IsMyday, ExpiredDateMyday)
        VALUES (?, ?, ?, 0, ?, ?, ?, ?, ?)
        """, (userID, title, description, important, due_date, created_date, is_myday, expired_date_myday))
        connection.commit()
        return cursor.lastrowid

    def get_all_tasks(self) -> List[Dict]:
        """
        Retrieve all tasks from the database.

        :return: List of tasks, each represented as a dictionary.
        """
        connection = db.connect_db()
        userID = localStorage.userID
        cursor = connection.execute("""
        SELECT * FROM Tasks t
        WHERE t.UserID = ?
        """, (userID))
        rows = cursor.fetchall()
        tasks = [
            {"id": row[0], "title": row[2], "description": row[3], "due_date": row[4], "completed": bool(row[5]), 
             "important": bool(row[6]), "is_myday": bool(row[7]), "created_date": row[8], "expired_date_myday": row[9]}
            for row in rows
        ]
        return tasks




    def get_a_task(self, task_id: int) -> Dict:
        connection = db.connect_db()
        userID = localStorage.userID
        cursor = connection.execute("""
                       SELECT * FROM Tasks t
                       WHERE t.UserID = ?
                       AND t.TaskID = ?
                       """, (userID, task_id))
        row = cursor.fetchone()
        if row is None:
            return None  # No task found with the given ID

        # Convert the row into a dictionary
        task = {
            "id": row[0],
            "title": row[2],
            "description": row[3],
            "due_date": row[4],
            "completed": bool(row[5]),
            "important": bool(row[6]),
            "is_myday": bool(row[7]),
            "created_date": row[8],
            "expired_date_myday": row[9]
        }
        return task

    def get_task_condition(self, title: str = None, description: str = None, completed: bool = None,
                           important: bool = None, due_date: str = None, created_date: str = None, is_myday: bool =
                           None, expired_date_myday: str = None, conditions_join_type: str = "AND") -> List[Dict]:
        """
        Queryr an existing task in the database.
        :param title: New title for the task (optional).
        :param description: New description for the task (optional).
        :param completed: New completion status for the task (optional).
        :param due_date: New due date for the task (optional).
        :param created_date: New created date for the task (optional).
        :param important: New important status for the task (optional).
        :param is_myday: New is_myday status for the task (optional).
        :param expired_date_myday: New expired date for the task (optional).

        :return: List of tasks, each represented as a dictionary.
        """
        conditions = []
        params = []

        if title is not None:
            conditions.append("Title = ?")
            params.append(title)
        if description is not None:
            conditions.append("Description = ?")
            params.append(description)
        if completed is not None:
            conditions.append("IsCompleted = ?")
            params.append(int(completed))  # SQLite uses 0/1 for BOOLEAN
        if due_date is not None:
            conditions.append("DueDate = ?")
            params.append(due_date)
        if created_date is not None:
            conditions.append("CreatedDate = ?")
            params.append(created_date)
        if important is not None:
            conditions.append("IsImportant = ?")
            params.append(important)
        if is_myday is not None:
            conditions.append("IsMyday = ?")
            params.append(is_myday)
        if expired_date_myday is not None:
            conditions.append("ExpiredDateMyday = ?")
            params.append(expired_date_myday)
        
        connection = db.connect_db()
        userID = localStorage.userID

        if conditions:
            conditions_query = f" {conditions_join_type.join(conditions)} "

            cursor = connection.execute((f"""
                        SELECT * FROM Tasks 
                        WHERE UserID = ?
                        AND {conditions_query}""", (userID)), params)
            rows = cursor.fetchall()
            if rows is None:
                return None
            tasks = [
                {"id": row[0], "title": row[2], "description": row[3], "due_date": row[4], "completed": bool(row[5]), 
                "important": bool(row[6]), "is_myday": bool(row[7]), "created_date": row[8], "expired_date_myday": row[9]}
                for row in rows
            ]
            return tasks
        return None

    def update_task(self, task_id: int, title: str = None, description: str = None, completed: bool = None, important: bool = None,
                    due_date: str = None, created_date: str = None, is_myday: bool = None, expired_date_myday: str = None):
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
        connection = db.connect_db()
        userID = localStorage.userID
        if title is not None:
            updates.append("Title = ?")
            params.append(title)
        if description is not None:
            updates.append("Description = ?")
            params.append(description)
        if completed is not None:
            updates.append("IsCompleted = ?")
            params.append(int(completed))  # SQLite uses 0/1 for BOOLEAN
        if due_date is not None:
            updates.append("DueDate = ?")
            params.append(due_date)
        if created_date is not None:
            updates.append("CreatedDate = ?")
            params.append(created_date)
        if important is not None:
            updates.append("IsImportant = ?")
            params.append(important)
        if is_myday is not None:
            updates.append("IsMyday = ?")
            params.append(is_myday)
        if expired_date_myday is not None:
            updates.append("ExpiredDateMyday = ?")
            params.append(expired_date_myday)

        if updates:
            query = f"UPDATE Tasks SET {', '.join(updates)} WHERE TaskID = ? AND UserID = {userID}"
            params.append(task_id)
            connection.execute(query, params)
            connection.commit()

    def delete_task(self, task_id: int):
        """
        Delete a task from the database.

        :param task_id: ID of the task to delete.
        """
        connection = db.connect_db()
        userID = localStorage.userID
        connection.execute("DELETE FROM Tasks WHERE UserID = ? AND TaskID = ?", (userID, task_id))
        connection.commit()

    def close_connection(self):
        """
        Close the connection to the database.
        """
        connection = db.connect_db()
        connection.close()


    #draft method
    # def add_column_if_not_exists(self, table_name, column_name, column_type):
    #     """
    #     Add a column to a SQLite table if it does not already exist.

    #     :param connection: SQLite database connection object.
    #     :param table_name: Name of the table to alter.
    #     :param column_name: Name of the column to add.
    #     :param column_type: Data type of the column (e.g., TEXT, INTEGER).
    #     """
    #     cursor = self.connection.cursor()

    #     # Check if the column exists
    #     cursor.execute(f"PRAGMA table_info({table_name})")
    #     columns = [row[1] for row in cursor.fetchall()]  # Column names are in the second position

    #     if column_name not in columns:
    #         # Add the column since it does not exist
    #         cursor.execute(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type}")
    #         print(f"Column '{column_name}' added to table '{table_name}'.")

    #     self.connection.commit()

if __name__ == "__main__":
    # Initialize the TaskModel
    model = TaskModel()

    # Add sample tasks
    # model.add_task("Buy groceries", "Milk, Bread, Eggs", "10/01/2024")
    # model.add_task("Submit report", "Complete Q4 report", "15/01/2024", important=True)
    # model.add_task("Clean the house", "Living room, Kitchen", "12/01/2024")
    # model.add_task("Workout", "Morning gym session", "11/01/2024", is_myday=True)

    print("Initial Tasks:")
    print(model.get_all_tasks())

    # Test get_task_condition for various scenarios
    print("\nTasks with title 'Buy groceries':")
    print(model.get_task_condition(title="Buy groceries"))

    print("\nImportant tasks:")
    print(model.get_task_condition(important=True))

    print("\nCompleted tasks:")
    print(model.get_task_condition(completed=True))

    print("\nTasks with due date '15/01/2024':")
    print(model.get_task_condition(due_date="15/01/2024"))

    print("\nTasks for 'My Day' and incompleted:")
    print(model.get_task_condition(is_myday=True, completed=False))

    print("\nTasks with description 'Living room, Kitchen':")
    print(model.get_task_condition(description="Living room, Kitchen"))

    # Close the connection
    model.close_connection()