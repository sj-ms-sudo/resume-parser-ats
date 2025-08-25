import sqlite3
conn = sqlite3.connect('resume.db')
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS resume(name TEXT , email TEXT , phone TEXT , skills TEXT , ats INTEGER)")
conn.commit()
conn.close()