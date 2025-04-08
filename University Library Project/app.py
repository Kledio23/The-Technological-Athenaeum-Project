from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)

app.secret_key = 'dksfjbhfsbhjdrgjhb'

@app.route('/')
def home():  # Check for user login
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
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()
        conn.close()
        if user:
            session['username'] = username
            return redirect(url_for('dashboard'))
        return render_template('login.html', error="User or password is incorrect. Please try again.")
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():  # Registration process
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect('users.db')  # Connects to SQL database to insert new information
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
        except sqlite3.IntegrityError:
            return "Username already exists."  # Returns error message if username already exists
        conn.close()
        return redirect(url_for('login'))  # Redirect to login after success
    return render_template('register.html')

@app.route('/logout')
def logout():  # Remove the user from the current session
    session.pop('username', None)
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

if __name__ == '__main__':
    app.run(debug=True)
