from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import pyotp
import qrcode
import io
import base64

app = Flask(__name__)

app.secret_key = 'dksfjbhfsbhjdrgjhb'

@app.route('/')
def home():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html', username=session['username'])

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, password, role, two_fa_enabled FROM users WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            session['user_id'] = user[0]
            session['username'] = user[1]
            session['role'] = user[3]
            if user[4]:
                return redirect(url_for('verify_2fa'))
            return redirect(url_for('dashboard'))

        return render_template('login.html', error="User or password is incorrect. Please try again.")
    
    return render_template('login.html')

@app.route('/verify_2fa', methods=['GET', 'POST'])
def verify_2fa():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        code = request.form['code']
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute("SELECT secret_key FROM users WHERE username = ?", (session['username'],))
        secret_key = cursor.fetchone()[0]
        conn.close()

        totp = pyotp.TOTP(secret_key)

        if totp.verify(code):
            session['2fa_verified'] = True  # Mark the 2FA as verified in the session
            return redirect(url_for('dashboard'))  # 2FA successful, redirect to dashboard
        return render_template('verify_2fa.html', error="Invalid 2FA code. Please try again.")
    
    return render_template('verify_2fa.html')

@app.route('/enable_2fa', methods=['GET', 'POST'])
def enable_2fa():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        # Generate a new TOTP secret key for the user
        secret_key = pyotp.random_base32()
        totp = pyotp.TOTP(secret_key)
        uri = totp.provisioning_uri(name=session['username'], issuer_name='YourLibraryApp')

        # Generate QR code for Google Authenticator
        img = qrcode.make(uri)
        buf = io.BytesIO()
        img.save(buf)
        buf.seek(0)
        img_base64 = base64.b64encode(buf.read()).decode('utf-8')

        # Save the secret key in the database
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET secret_key = ?, two_fa_enabled = 1 WHERE username = ?", (secret_key, session['username']))
        conn.commit()
        conn.close()

        return render_template('enable_2fa.html', img_base64=img_base64)  # Show QR code for scanning
    
    return render_template('enable_2fa.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
        except sqlite3.IntegrityError:
            return "Username already exists."
        conn.close()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/admin-dashboard', methods=['GET', 'POST'])
def admin_dashboard():
    if 'username' not in session or session.get('role') != 'admin':
        return redirect(url_for('login'))

    return render_template('admin_dashboard.html')

@app.route('/modify-books', methods=['GET', 'POST'])
def modify_books():
    if 'username' not in session or session.get('role') != 'admin':
        return redirect(url_for('login'))

    conn_books = sqlite3.connect('library.db')
    cursor_books = conn_books.cursor()
    message = None

    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        isbn = request.form['isbn']
        availability = 'available'
        cursor_books.execute("INSERT INTO books (title, author, isbn, availability) VALUES (?, ?, ?, ?)", 
                             (title, author, isbn, availability))
        conn_books.commit()
        message = "Book added successfully!"

        conn_users = sqlite3.connect('users.db')
        cursor_users = conn_users.cursor()

        cursor_users.execute("SELECT id FROM users")
        users = cursor_users.fetchall()

        conn_users.close()

        conn_notifications = sqlite3.connect('notifications.db')
        cursor_notifications = conn_notifications.cursor()

        for user in users:
            cursor_notifications.execute('''
                INSERT INTO notifications (type, title, user_id, link) 
                VALUES (?, ?, ?, ?)
            ''', ('book', f'New Book: {title} by {author}', user[0], f'/books/{isbn}'))

        conn_notifications.commit()
        conn_notifications.close()

    cursor_books.execute("SELECT * FROM books")
    books = cursor_books.fetchall()
    conn_books.close()

    return render_template('modify_books.html', books=books, message=message)

@app.route('/remove-book/<string:isbn>', methods=['POST'])
def remove_book(isbn):
    if 'username' not in session or session.get('role') != 'admin':
        return redirect(url_for('login'))
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM books WHERE isbn = ?", (isbn,))
    conn.commit()
    conn.close()
    return redirect(url_for('modify_books'))

@app.route('/edit-book/<string:isbn>', methods=['GET', 'POST'])
def edit_book(isbn):
    if 'username' not in session or session.get('role') != 'admin':
        return redirect(url_for('login'))

    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()

    if request.method == 'POST':
        isbn = request.form['isbn']
        title = request.form['title']
        author = request.form['author']
        cursor.execute("UPDATE books SET isbn = ?, title = ?, author = ? WHERE isbn = ?",
                       (isbn, title, author, isbn))
        conn.commit()
        conn.close()
        return redirect(url_for('modify_books'))

    cursor.execute("SELECT * FROM books WHERE isbn = ?", (isbn,))
    book = cursor.fetchone()
    conn.close()

    return render_template('edit_book.html', book=book)

@app.route('/modify-events', methods=['GET', 'POST'])
def modify_events():
    if 'username' not in session or session.get('role') != 'admin':
        return redirect(url_for('login'))

    conn_events = sqlite3.connect('events.db')
    cursor_events = conn_events.cursor()
    message = None

    if request.method == 'POST':
        event = request.form['event']
        date = request.form['date']
        location = request.form['location']
        description = request.form['description']

        cursor_events.execute("INSERT INTO events (event, date, location, description) VALUES (?, ?, ?, ?)", 
                              (event, date, location, description))
        conn_events.commit()
        message = "Event added successfully!"

        conn_users = sqlite3.connect('users.db')
        cursor_users = conn_users.cursor()

        cursor_users.execute("SELECT id FROM users")
        users = cursor_users.fetchall()

        conn_users.close()

        conn_notifications = sqlite3.connect('notifications.db')
        cursor_notifications = conn_notifications.cursor()

        for user in users:
            cursor_notifications.execute('''
                INSERT INTO notifications (type, title, user_id, link) 
                VALUES (?, ?, ?, ?)
            ''', ('event', f'New Event: {event}', user[0], f'/events/{event}'))

        conn_notifications.commit()
        conn_notifications.close()

    cursor_events.execute("SELECT * FROM events")
    events = cursor_events.fetchall()
    conn_events.close()

    return render_template('modify_events.html', events=events, message=message)

@app.route('/remove-event/<string:event>', methods=['POST'])
def remove_event(event):
    if 'username' not in session or session.get('role') != 'admin':
        return redirect(url_for('login'))
    
    conn = sqlite3.connect('events.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM events WHERE event = ?", (event,))
    conn.commit()
    conn.close()
    return redirect(url_for('modify_events'))

@app.route('/edit-event/<string:event_id>', methods=['GET', 'POST'])
def edit_event(event_id):
    if 'username' not in session or session.get('role') != 'admin':
        return redirect(url_for('login'))

    conn = sqlite3.connect('events.db')
    cursor = conn.cursor()

    if request.method == 'POST':
        event_name = request.form['event']
        date = request.form['date']
        location = request.form['location']
        description = request.form['description']
        
        cursor.execute("UPDATE events SET event = ?, date = ?, location = ?, description = ? WHERE event_id = ?",
                       (event_name, date, location, description, event_id))
        conn.commit()
        conn.close()
        return redirect(url_for('modify_events'))

    cursor.execute("SELECT * FROM events WHERE event_id = ?", (event_id,))
    event_data = cursor.fetchone()
    conn.close()

    return render_template('edit_event.html', event=event_data)

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('2fa_verified', None)  # Clear the 2FA verification session data on logout
    return redirect(url_for('login'))

@app.route('/catalog', methods=['GET', 'POST'])
def catalog():
    if 'username' not in session:
        return redirect(url_for('login'))

    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()

    if request.method == 'POST':  # Performs the search based on title
        search_query = request.form['search']
        cursor.execute("SELECT * FROM books WHERE title LIKE ?", ('%' + search_query + '%',))
    else:
        cursor.execute("SELECT * FROM books")  # Displays all books if no search

    books = cursor.fetchall()
    conn.close()

    return render_template('catalog.html', books=books)

@app.route('/reserve/<isbn>', methods=['POST'])
def reserve_book(isbn):
    if 'username' not in session:  # Makes sure user is logged in
        return redirect(url_for('login'))

    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()

    cursor.execute("SELECT availability, reserved_by FROM books WHERE isbn = ?", (isbn,))
    book = cursor.fetchone()

    if not book:
        conn.close()
        return "Book not found."  # Error message if book not found

    availability, reserved_by = book

    if availability == 'available' and reserved_by is None:  # Checks if book is available & not reserved
        cursor.execute("UPDATE books SET reserved_by = ? WHERE isbn = ?", (session['username'], isbn))
        cursor.execute("UPDATE books SET availability = 'reserved' WHERE isbn = ?", (isbn,))
        conn.commit()
        conn.close()
        return redirect(url_for('catalog'))

    conn.close()
    return "This book is already reserved."

@app.route('/return/<isbn>', methods=['POST'])
def return_book(isbn):
    if 'username' not in session:
        return redirect(url_for('login'))

    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()

    cursor.execute("SELECT availability, reserved_by FROM books WHERE isbn = ?", (isbn,))
    book = cursor.fetchone()

    if not book:
        conn.close()
        return "Book not found."

    availability, reserved_by = book

    if reserved_by == session['username']:
        cursor.execute("UPDATE books SET reserved_by = NULL WHERE isbn = ?", (isbn,))
        cursor.execute("UPDATE books SET availability = 'available' WHERE isbn = ?", (isbn,))
        conn.commit()
        conn.close()
        return redirect(url_for('my_books'))  # Redirect back to the My Books page

    conn.close()
    return "You haven't reserved this book."

@app.route('/my-books')
def my_books():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    username = session['username']
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()

    # Query for the books that are reserved by the logged-in user, without including due_date
    cursor.execute("SELECT title, author, isbn FROM books WHERE reserved_by = ?", (username,))
    books = cursor.fetchall()
    conn.close()

    return render_template('my_books.html', books=books)

@app.route('/notifications')
def notifications():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']

    conn = sqlite3.connect('notifications.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM notifications WHERE user_id = ?", (user_id,))
    notifications = cursor.fetchall()
    conn.close()

    return render_template('notifications.html', notifications=notifications)

@app.route('/upcoming-events')
def upcoming_events():
    conn = sqlite3.connect('events.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM events")
    events = cursor.fetchall()
    conn.close()
    return render_template('upcoming_events.html', events=events)

@app.route('/account')
def manage_account():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('manage_account.html')

@app.route('/edit-account', methods=['GET', 'POST'])
def edit_account():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        current_password = request.form['current_password']
        new_password = request.form['new_password']

        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (session['username'],))
        user = cursor.fetchone()

        if user and user[1] == current_password:
            cursor.execute("UPDATE users SET password = ? WHERE username = ?", (new_password, session['username']))
            conn.commit()
            conn.close()
            return render_template('edit_account.html', message="Password successfully updated.")

        conn.close()
        return render_template('edit_account.html', error="Current password is incorrect. Please try again.")
    
    return render_template('edit_account.html')

if __name__ == '__main__':
    app.run(debug=True)
