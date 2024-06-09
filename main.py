from website import create_app, db
from website.models import User, Book
from werkzeug.security import generate_password_hash
import logging
from flask import session
from os import path

# Create the Flask app
app = create_app()

# Configure logging
logging.basicConfig(filename='app.log', level=logging.INFO)

# Function to log session information
def log_session_info():
    if 'user' in session:
        logging.info(f"Session ID: {session.get('_id')}, User Email: {session.get('user_email')}, User Role: {session.get('user_role')}")

# Register the log_session_info function to run before each request
@app.before_request
def before_request():
    log_session_info()

# Function to create the database if it doesn't exist
def create_database():
    with app.app_context():
        if not path.exists('website/' + app.config['SQLALCHEMY_DATABASE_URI']):
            db.create_all()
            print('Created Database!')

# Function to add books to the database
def add_books():
    # Ensure we are working within the application context
    with app.app_context():
        # Define a list of books with their details
        books_data = [
            {"title": "Book 1", "author": "Author 1", "file_path": "/path/to/book1.pdf"},
            {"title": "Book 2", "author": "Author 2", "file_path": "/path/to/book2.pdf"},
            {"title": "Book 3", "author": "Author 3", "file_path": "/path/to/book3.pdf"},
            # Add more books as needed
        ]

        # Add each book to the database
        for book_info in books_data:
            book = Book.query.filter_by(title=book_info['title']).first()
            if not book:
                new_book = Book(title=book_info['title'], author=book_info['author'], file_path=book_info['file_path'])
                db.session.add(new_book)
        db.session.commit()

# Function to create admin user
def create_admin():
    with app.app_context():
        # Check if admin user already exists
        admin = User.query.filter_by(email='admin@example.com').first()
        if not admin:
            admin_password = generate_password_hash('AdminPass123!', method='sha256')
            admin = User(email='admin@example.com', password=admin_password, first_name='Admin', role='admin')
            db.session.add(admin)
            db.session.commit()

# Call the functions to create the database, add books, and create admin user when the application starts
create_database()
add_books()
create_admin()

# Run the app
if __name__ == '__main__':
    app.run(debug=True)