import sqlite3

conn = sqlite3.connect('events.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS events (
        event_id INTEGER PRIMARY KEY AUTOINCREMENT,
        event TEXT NOT NULL,
        date TEXT NOT NULL,
        location TEXT NOT NULL,
        description TEXT
    )
''')

conn.commit()
conn.close()