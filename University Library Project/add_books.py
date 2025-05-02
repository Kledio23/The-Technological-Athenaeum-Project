import sqlite3

conn = sqlite3.connect('library.db')
cursor = conn.cursor()

cursor.execute('DELETE FROM books')

cursor.executemany('''
    INSERT INTO books (isbn, title, author, availability, reserved_by) VALUES (?, ?, ?, ?, ?)
''', [
    ('9780060935467', 'To Kill a Mockingbird', 'Harper Lee', 'available', None),
    ('9780451524935', '1984', 'George Orwell', 'available', None),
    ('9781451673265', 'Fahrenheit 451', 'Ray Bradbury', 'available', None),
    ('9780743273565', 'The Great Gatsby', 'F. Scott Fitzgerald', 'available', None),
    ('9780143105954', 'Moby-Dick', 'Herman Melville', 'available', None),
    ('9781250230782', 'The Silent Patient', 'Alex Michaelides', 'available', None),
    ('9780307387899', 'The Road', 'Cormac McCarthy', 'available', None),
    ('9781594634024', 'The Girl on the Train', 'Paula Hawkins', 'available', None),
    ('9780735219106', 'Where the Crawdads Sing', 'Delia Owens', 'available', None),
    ('9780316556323', 'Circe', 'Madeline Miller', 'available', None),
    ('9780307744432', 'The Night Circus', 'Erin Morgenstern', 'available', None),
    ('9780425274866', 'Big Little Lies', 'Liane Moriarty', 'available', None),
    ('9780547928227', 'The Hobbit', 'J.R.R. Tolkien', 'available', None),
    ('9780375842207', 'The Book Thief', 'Markus Zusak', 'available', None),
    ('9780062315007', 'The Alchemist', 'Paulo Coelho', 'available', None),
    ('9781339016573', 'The Hunger Games', 'Suzanne Collins', 'available', None),
    ('9780525478812', 'The Fault in Our Stars', 'John Green', 'available', None),
    ('9780385333849', 'Slaughterhouse-Five', 'Kurt Vonnegut', 'available', None),
    ('9780345806789', 'The Shining', 'Stephen King', 'available', None),
    ('9780143039433', 'The Grapes of Wrath', 'John Steinbeck', 'available', None),
    ('9780425232200', 'The Help', 'Kathryn Stockett', 'available', None),
    ('9781616208684', 'An American Marriage', 'Tayari Jones', 'available', None),
    ('9781501105777', 'Before We Were Strangers', 'Renée Carlino', 'available', None),
    ('9781250316776', 'Red, White & Royal Blue', 'Casey McQuiston', 'available', None),
    ('9781476729091', 'The Rosie Project', 'Graeme Simsion', 'available', None),
    ('9781982134198', 'The Paris Library', 'Janet Skeslien Charles', 'available', None),
    ('9780062671196', 'The Night Watchman', 'Louise Erdrich', 'available', None),
    ('9780062678423', 'The Woman in the Window', 'A.J. Finn', 'available', None),
    ('9781984822185', 'Normal People', 'Sally Rooney', 'available', None),
    ('9781250178619', 'The Four Winds', 'Kristin Hannah', 'available', None),
    ('9780735220690', 'Eleanor Oliphant Is Completely Fine', 'Gail Honeyman', 'available', None),
    ('9781250229533', 'The Great Alone', 'Kristin Hannah', 'available', None),
    ('9781250175465', 'The Night Tiger', 'Yangsze Choo', 'available', None),
    ('9781501190117', 'The Family Upstairs', 'Lisa Jewell', 'available', None),
    ('9780525559498', 'The Midnight Library', 'Matt Haig', 'available', None),
    ('9781451681758', 'The Light Between Oceans', 'M.L. Stedman', 'available', None),
    ('9780062797155', 'The Tattooist of Auschwitz', 'Heather Morris', 'available', None),
    ('9780062654199', 'The Alice Network', 'Kate Quinn', 'available', None),
    ('9781476738024', 'A Man Called Ove', 'Fredrik Backman', 'available', None),
    ('9781524746094', 'The Girl with the Louding Voice', 'Abi Daré', 'available', None),
    ('9781435158184', 'The Secret Garden', 'Frances Hodgson Burnett', 'available', None),
    ('9780735224315', 'Little Fires Everywhere', 'Celeste Ng', 'available', None),
    ('9781878424310', 'The Four Agreements', 'Don Miguel Ruiz', 'available', None),
    ('9780142407332', 'The Outsiders', 'S.E. Hinton', 'available', None),
    ('9780735215092', 'The Immortalists', 'Chloe Benjamin', 'available', None)
])

conn.commit()
conn.close()
