from .models import Book, db

def add_books():
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

# Call the function to add books when the application starts
add_books()