import sqlite3 as sq

db = sq.connect('database.db')
cur = db.cursor()

cur.execute('''  
    CREATE TABLE IF NOT EXISTS admin(
    id INTEGER PRIMARY KEY,
    tg INTEGER
    )''')

# with sq.connect('database.db'):
# 	cur.execute("INSERT INTO admin (tg) VALUES (?)", (825627855,))
# 	db.commit()