from flask import Flask, request, jsonify, make_response
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_cors import CORS
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
import os
app = Flask(__name__)

# Enable CORS for the frontend and allow credentials (cookies)
CORS(app, origins=["https://map-6aha.onrender.com", "https://hamed12142212.github.io"], supports_credentials=True)


# Configurations
app.config["JWT_SECRET_KEY"] = "your_jwt_secret_key"  # Secret key for JWT
app.config['SQLALCHEMY_DATABASE_URI'] = (
    "postgresql://usersdata_fyx5_user:n3z4c1YAQ3SLVuj7raLsKYgQXZZ2eT5p"
    "@dpg-csr93maj1k6c7394uh1g-a.frankfurt-postgres.render.com/usersdata_fyx5?sslmode=require"
)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking

jwt = JWTManager(app)
db = SQLAlchemy(app)  # Initialize the database

# Create the User model
class User(db.Model):
    __tablename__ = 'users'  # Explicitly setting the table name to 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"<User {self.username}>"




# Route for login (accepts both GET and POST)
@app.route("/", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Handle login and return a JWT token
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")
        
        # Query the user from the database
        user = User.query.filter_by(username=username).first()
        
        if user and user.password == password:
            # Generate the JWT token
            access_token = create_access_token(identity=username)
            
            # Create a response object
            response = make_response(jsonify(msg="Login successful", access_token=access_token))
            
            # Set the JWT token in a cookie (with HttpOnly and SameSite attributes)
            response.set_cookie("access_token_cookie", access_token, max_age=timedelta(days=1), httponly=True, samesite='None', secure=True, path='/')

            return response
        else:
            return jsonify(msg="Invalid username or password"), 401

    elif request.method == 'GET':
        # If the user tries to check if they are logged in
        if "access_token_cookie" in request.cookies:
            return jsonify(msg="You are logged in")
        else:
            return jsonify(msg="You are not logged in"), 401

# Protected route that requires authentication
@app.route("/protected", methods=["GET", "POST"])
@jwt_required(locations=["cookies"])  # Ensure the JWT is in the cookies
def protected():
    return jsonify(msg="Access granted to protected resource")

# Route to check if the token is valid
@app.route("/check_token", methods=["GET"])
@jwt_required(locations=["cookies"])  # Look for the token in cookies
def check_token():
    current_user = get_jwt_identity()  # Get the current user's identity from the JWT
    return jsonify(msg=f"The token is valid! Logged in as {current_user}")

# Route for logout (clear the JWT token)
@app.route("/logout", methods=["POST"])
@jwt_required(locations=["cookies"])  # Look for the token in cookies
def logout():
    response = make_response(jsonify(msg="Logged out successfully"))
    response.delete_cookie("access_token_cookie")
    return response

@app.route("/test-db")
def test_db():
    try:
        user_count = User.query.count()  # This counts users in the 'users' table
        return jsonify({"message": f"Connection successful! User count: {user_count}"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500



if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=int(os.getenv('PORT', 5000)))
