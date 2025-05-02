import sqlite3

conn = sqlite3.connect('users.db')
cursor = conn.cursor()

cursor.execute('''
    UPDATE users
    SET role = 'admin'
    WHERE username = 'admin'
''')

conn.commit()
conn.close()