from flask import Blueprint, render_template, request, send_from_directory, redirect,url_for,flash,current_app, send_file
from flask_login import  login_required, current_user
from .models import Book
from random import sample
import os
from . import db


views = Blueprint('views', __name__)


from .models import User

@views.route('/admin-home', methods=['GET', 'POST'])
@login_required
def admin_home():
    if current_user.role != 'admin':
        flash('Access denied: Only admins can access this page.', category='error')
        return redirect(url_for('views.home'))
    
    # Fetch all users from the database
    all_users = User.query.all()

    # Fetch all books from the database
    all_books = Book.query.all()

    return render_template('admin_home.html', user=current_user, users=all_users, books=all_books)



@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        query = request.form.get('query')
        # Perform a case-insensitive search for books matching the query
        search_results = Book.query.filter(Book.title.ilike(f"%{query}%") | Book.author.ilike(f"%{query}%")).all()
        return render_template('search_results.html', user=current_user, search_results=search_results)
    
    # Fetch top 3 random books for display
    all_books = Book.query.all()
    top_books = sample(all_books, min(3, len(all_books)))

    return render_template('home.html', user=current_user, top_books=top_books)




from flask import session

@views.route('/download/<int:book_id>')
@login_required
def download_book(book_id):
    # Define the path to the dummy text file
    dummy_text_path = '/Users/furqaanm/Desktop/IT_Infra_Project/dummy_text.txt'

    # Check if the dummy text file exists
    if not os.path.exists(dummy_text_path):
        flash('Dummy text file not found.', category='error')
        return redirect(url_for('views.home'))

    # Include session key as a query parameter in the download link
    download_link = url_for('views.download_file', _external=True, session_key=session.get('_id'))

    # Redirect to the download link
    return redirect(download_link)

@views.route('/download_file')
@login_required
def download_file():
    session_key = request.args.get('session_key')
    # Check if the session key matches the expected value
    if session_key != session.get('_id'):
        flash('Unauthorized access.', category='error')
        return redirect(url_for('views.home'))

    # Define the path to the dummy text file
    dummy_text_path = '/Users/furqaanm/Desktop/IT_Infra_Project/dummy_text.txt'



    # Check if the dummy text file exists
    if not os.path.exists(dummy_text_path):
        flash('Dummy text file not found.', category='error')
        return redirect(url_for('views.home'))

    # Send the dummy text file to the user for download
    return send_file(dummy_text_path, as_attachment=True)



@views.route('/delete-user/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    # Check if the current user is an admin
    if current_user.is_authenticated and current_user.role == 'admin':
        # Query the user to be deleted
        user_to_delete = User.query.get(user_id)
        if user_to_delete:
            # Delete the user
            db.session.delete(user_to_delete)
            db.session.commit()
            flash('User deleted successfully!', 'success')
        else:
            flash('User not found!', 'error')
    else:
        flash('You do not have permission to perform this action!', 'error')

    # Redirect to the appropriate page after deletion
    return redirect(url_for('views.admin_home'))



@views.route('/add-book', methods=['GET', 'POST'])
@login_required
def add_book():
    if current_user.role != 'admin':
        flash('Access denied: Only admins can access this page.', category='error')
        return redirect(url_for('views.home'))

    if request.method == 'POST':
        title = request.form.get('title')
        author = request.form.get('author')
        file_path = request.form.get('file_path')

        if not title or not author or not file_path:
            flash('All fields are required.', category='error')
        else:
            new_book = Book(title=title, author=author, file_path=file_path)
            db.session.add(new_book)
            db.session.commit()
            flash('Book added successfully!', category='success')

    return render_template('add_book.html', user=current_user)


@views.route('/delete-book/<int:book_id>', methods=['POST'])
@login_required
def delete_book(book_id):
    if current_user.role != 'admin':
        flash('Access denied: Only admins can access this page.', category='error')
        return redirect(url_for('views.home'))

    book = Book.query.get(book_id)
    if not book:
        flash('Book not found.', category='error')
    else:
        db.session.delete(book)
        db.session.commit()
        flash('Book deleted successfully!', category='success')

    return redirect(url_for('views.admin_home'))
