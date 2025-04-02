import sqlite3

conn = sqlite3.connect('library.db')

cursor = conn.cursor()

cursor.execute('DELETE FROM books')

cursor.executemany('''
    INSERT INTO books (isbn, title, author, availability) VALUES (?, ?, ?, ?)
''', [
    ('9780061120084', 'To Kill a Mockingbird', 'Harper Lee', 'available'),
    ('9780451524935', '1984', 'George Orwell', 'available'),
    ('9781451673319', 'Fahrenheit 451', 'Ray Bradbury', 'available'),
    ('9781982149482', 'The Great Gatsby', 'F. Scott Fitzgerald', 'available'),
    ('9780143105954', 'Moby-Dick', 'Herman Melville', 'available'),
    ('9781250230782', 'The Silent Patient', 'Alex Michaelides', 'available'),
    ('9780307387899', 'The Road', 'Cormac McCarthy', 'available'),
    ('9781594634024', 'The Girl on the Train', 'Paula Hawkins', 'available'),
    ('9780062315014', 'Where the Crawdads Sing', 'Delia Owens', 'available'),
    ('9781250015740', 'Circe', 'Madeline Miller', 'available'),
    ('9781784074643', 'The Night Circus', 'Erin Morgenstern', 'available'),
    ('9780062641557', 'Educated', 'Tara Westover', 'available'),
    ('9781250090499', 'The Seven Husbands of Evelyn Hugo', 'Taylor Jenkins Reid', 'available'),
    ('9780062420718', 'Big Little Lies', 'Liane Moriarty', 'available'),
    ('9781566199100', 'The Hobbit', 'J.R.R. Tolkien', 'available'),
    ('9780060935474', 'The Book Thief', 'Markus Zusak', 'available'),
    ('9780142000687', 'The Alchemist', 'Paulo Coelho', 'available'),
    ('9780345482962', 'The Hunger Games', 'Suzanne Collins', 'available'),
    ('9781416544820', 'The Fault in Our Stars', 'John Green', 'available'),
    ('9780671027366', 'Slaughterhouse-Five', 'Kurt Vonnegut', 'available'),
    ('9780446670785', 'The Shining', 'Stephen King', 'available'),
    ('9780394590315', 'The Grapes of Wrath', 'John Steinbeck', 'available'),
    ('9781439168999', 'The Help', 'Kathryn Stockett', 'available'),
    ('9781501125355', 'An American Marriage', 'Tayari Jones', 'available'),
    ('9780062982643', 'Before We Were Strangers', 'Renée Carlino', 'available'),
    ('9781250079579', 'Red, White & Royal Blue', 'Casey McQuiston', 'available'),
    ('9781250075717', 'The Rosie Project', 'Graeme Simsion', 'available'),
    ('9781400069948', 'The Paris Library', 'Janet Skeslien Charles', 'available'),
    ('9780345514005', 'The Night Watchman', 'Louise Erdrich', 'available'),
    ('9780375711208', 'The Woman in the Window', 'A.J. Finn', 'available'),
    ('9781250168732', 'Normal People', 'Sally Rooney', 'available'),
    ('9781501151439', 'The Four Winds', 'Kristin Hannah', 'available'),
    ('9780062287561', 'Eleanor Oliphant Is Completely Fine', 'Gail Honeyman', 'available'),
    ('9780062258158', 'The Great Alone', 'Kristin Hannah', 'available'),
    ('9781500115303', 'The Night Tiger', 'Yangsze Choo', 'available'),
    ('9780345544732', 'The Family Upstairs', 'Lisa Jewell', 'available'),
    ('9780062267487', 'The Midnight Library', 'Matt Haig', 'available'),
    ('9780061999268', 'The Light Between Oceans', 'M.L. Stedman', 'available'),
    ('9780062358044', 'The Couple Next Door', 'Shari Lapena', 'available'),
    ('9780525954609', 'The Tattooist of Auschwitz', 'Heather Morris', 'available'),
    ('9781476758000', 'The Alice Network', 'Kate Quinn', 'available'),
    ('9781250064731', 'A Man Called Ove', 'Fredrik Backman', 'available'),
    ('9780385351404', 'The Girl with the Louding Voice', 'Abi Daré', 'available'),
    ('9780395315649', 'The Secret Garden', 'Frances Hodgson Burnett', 'available'),
    ('9780060838669', 'The Help', 'Kathryn Stockett', 'available'),
    ('9781250061075', 'Little Fires Everywhere', 'Celeste Ng', 'available'),
    ('9780316102041', 'Big Little Lies', 'Liane Moriarty', 'available'),
    ('9780141036149', 'The Silent Patient', 'Alex Michaelides', 'available'),
    ('9781476792647', 'The Night Watchman', 'Louise Erdrich', 'available'),
    ('9781250078053', 'Red, White & Royal Blue', 'Casey McQuiston', 'available'),
    ('9781250019138', 'The Night Circus', 'Erin Morgenstern', 'available'),
    ('9781476744041', 'The Four Agreements', 'Don Miguel Ruiz', 'available'),
    ('9780061131741', 'The Outsiders', 'S.E. Hinton', 'available'),
    ('9780374182356', 'The Immortalists', 'Chloe Benjamin', 'available'),
    ('9780316113303', 'The Rosie Project', 'Graeme Simsion', 'available'),
    ('9780062868231', 'The Book Thief', 'Markus Zusak', 'available'),
    ('9781501145529', 'The Silent Corner', 'Dean Koontz', 'available')
])

conn.commit()

conn.close()