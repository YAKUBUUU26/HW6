from flask import Flask, request, jsonify, abort
import json
import os
import secrets

app = Flask(__name__)

# Loading users from a file
USER_FILE = "../../Scripts/users.json"

# Loading or initializing user data
if os.path.exists(USER_FILE):
    with open(USER_FILE, 'r') as f:
        users = json.load(f)
else:
    users = {}


# Save users to the file
def save_users():
    with open(USER_FILE, 'w') as f:
        json.dump(users, f, indent=4)


# Helper function to authenticate users by email and API key
def authenticate(email, api_key):
    user = users.get(email)
    if not user or user.get("api_key") != api_key:
        abort(403, "Unauthorized access")
    return email


@app.route('/users', methods=['POST'])
def add_user():
    """Add a new user via form or JSON data"""
    data = request.form if request.form else request.json
    email = data.get('email')
    age = data.get('age')

    if not email or not age:
        return jsonify({"error": "Email and age are required"}), 400
    if email in users:
        return jsonify({"error": "User already exists"}), 400

    # Generate an API key for the user
    api_key = secrets.token_hex(16)

    # Add user to the database
    users[email] = {"email": email, "age": age, "api_key": api_key}
    save_users()
    return jsonify({"message": "User added successfully", "api_key": api_key}), 201


@app.route('/users/<email>', methods=['GET'])
def get_user(email):
    """Retrieve user profile"""
    api_key = request.headers.get('API-Key')
    authenticate(email, api_key)
    return jsonify(users[email])


@app.route('/users/<email>', methods=['PUT'])
def update_user(email):
    """Update a user's profile information"""
    api_key = request.headers.get('API-Key')
    authenticate(email, api_key)

    data = request.form if request.form else request.json
    age = data.get('age')

    if not age:
        return jsonify({"error": "Age is required"}), 400

    # Update the user's age
    users[email]["age"] = age
    save_users()
    return jsonify({"message": "User updated successfully"})


@app.route('/users/<email>', methods=['DELETE'])
def delete_user(email):
    """Delete a user's profile"""
    api_key = request.headers.get('API-Key')
    authenticate(email, api_key)
    users.pop(email, None)
    save_users()
    return jsonify({"message": "User deleted successfully"})


@app.route('/')
def home():
    return "Welcome to the User API!"


if __name__ == "__main__":
    app.run(debug=True)
