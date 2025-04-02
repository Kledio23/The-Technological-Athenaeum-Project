import sqlite3

conn = sqlite3.connect('library.db')
cursor = conn.cursor()

cursor.execute
('''
    ALTER TABLE books ADD COLUMN reserved_by TEXT
''')

conn.commit()

conn.close()