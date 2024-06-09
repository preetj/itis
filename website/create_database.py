# create_database.py

from website import db, create_app
from website import User, Book
from werkzeug.security import generate_password_hash

def create_admin():
    admin = User(
        email='admin@example.com',
        password=generate_password_hash('AdminPass123!', method='sha256'),
        first_name='Admin',
        role='admin'
    )
    db.session.add(admin)
    db.session.commit()

def create_db_and_admin():
    app = create_app()
    with app.app_context():
        db.create_all()
        create_admin()

if __name__ == "__main__":
    create_db_and_admin()
