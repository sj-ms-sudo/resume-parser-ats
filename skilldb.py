import sqlite3
conn = sqlite3.connect('skills.db')
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS skills(Skills TEXT)")
conn.commit()
conn.close()