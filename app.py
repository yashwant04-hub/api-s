from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory list to store users
users = []

# Home route (shows welcome message)
@app.route('/')
def home():
    return """
    <h1>User Management API</h1>
    <p>Use the following endpoints:</p>
    <ul>
        <li>GET /users</li>
        <li>GET /users/&lt;id&gt;</li>
        <li>POST /users</li>
        <li>PUT /users/&lt;id&gt;</li>
        <li>DELETE /users/&lt;id&gt;</li>
    </ul>
    """

# Helper: Find user by ID
def find_user(user_id):
    return next((user for user in users if user['id'] == user_id), None)

# Get all users
@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(users), 200

# Get user by ID
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = find_user(user_id)
    if user:
        return jsonify(user), 200
    return jsonify({'error': 'User not found'}), 404

# Add a new user
@app.route('/users', methods=['POST'])
def add_user():
    data = request.get_json()
    if not data or 'id' not in data or 'name' not in data or 'email' not in data:
        return jsonify({'error': 'Invalid user data'}), 400

    if find_user(data['id']):
        return jsonify({'error': 'User ID already exists'}), 400

    users.append({
        'id': data['id'],
        'name': data['name'],
        'email': data['email']
    })
    return jsonify({'message': 'User added successfully'}), 201

# Update existing user
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = find_user(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    user['name'] = data.get('name', user['name'])
    user['email'] = data.get('email', user['email'])

    return jsonify({'message': 'User updated successfully'}), 200

# Delete user
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = find_user(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    users.remove(user)
    return jsonify({'message': 'User deleted successfully'}), 200

if __name__ == '__main__':
    app.run(debug=True)
