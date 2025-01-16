from context import database as db
    
db = db.connect_db()
cursor = db.execute("SELECT * FROM Users u WHERE u.UserName = ? AND u.Password = ?", ('admin', 'root'))

result = cursor.fetchall()
print(result[0][0])

# from context import localStorage


# print(localStorage.userID)

# localStorage.userID = 1

# print(localStorage.userID)