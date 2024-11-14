from app import app, db, User  # Import your Flask app and models

# Adding a user manually
def add_user(username, password):
    with app.app_context():  # Ensure this code runs inside an app context
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()

# Add users
add_user('hamed', '123')
add_user('aa', '123')

print("Users added successfully!")
