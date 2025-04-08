import sqlite3

conn = sqlite3.connect('library.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS books
    (
        isbn TEXT PRIMARY KEY,
        title TEXT NOT NULL,
        author TEXT NOT NULL,
        availability TEXT NOT NULL DEFAULT 'available'
    )
''')

conn.commit()

conn.close()