import sqlite3

conn = sqlite3.connect('library.db')

cursor = conn.cursor()
cursor.execute('DELETE FROM books')

cursor.executemany('''
    INSERT INTO books (isbn, title, author, availability) VALUES (?, ?, ?, ?)
''', [
    ('9780061120084', 'To Kill a Mockingbird', 'Harper Lee', 'available'),
    ('9780451524935', '1984', 'George Orwell', 'available'),
    ('9781451673319', 'Fahrenheit 451', 'Ray Bradbury', 'available')
    ('9781451673319', 'Fahr', 'Ray ', 'available')
])

conn.commit()

conn.close()