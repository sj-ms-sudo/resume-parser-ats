import sqlite3
from werkzeug.security import generate_password_hash
conn = sqlite3.connect('users.db')
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS users(username TEXT , password TEXT)")
username = 'Admin'
pw = generate_password_hash("admin123")
c.execute("INSERT INTO users (username,password) VALUES (?,?)",(username,pw))
conn.commit()
conn.close()