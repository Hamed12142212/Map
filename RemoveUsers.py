from app import app, db, User

def delete_user(username):
    with app.app_context():  # Ensure this runs inside the Flask app context
        # Find the user by the username
        user = User.query.filter_by(username=username).first()
        
        if user:
            db.session.delete(user)  # Delete the user
            db.session.commit()  # Commit the changes to the database
            print(f"User '{username}' deleted successfully!")
        else:
            print(f"User '{username}' not found.")

# Delete a user by username
delete_user('aa')  # Replace 'user1' with the username you want to delete
