from app import app, db, User  # Import the app, db, and User model

def get_all_users():
    with app.app_context():  # Ensure this code runs inside an app context
        users = User.query.all()  # Get all users from the database
        for user in users:
            print(f"Username: {user.username}, Password: {user.password}")

# Display all users
get_all_users()
