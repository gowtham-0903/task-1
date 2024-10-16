from flask import Flask, jsonify, request
from pymongo import MongoClient

app = Flask(__name__)

# Initialize MongoDB connection
mongo_uri = "mongodb://localhost:27017/"  # Update as needed
client = MongoClient(mongo_uri)
db = client['health_db']  # Replace with your database name

# Fetch all users
@app.route('/api/users', methods=['GET'])
def get_users():
    users = list(db.users.find({}, {'_id': 0, 'username': 1, 'timezone': 1, 'version': 1, 'app': 1, 'country': 1}))
    return jsonify(users)

# Debugging code: Print out user info
@app.route('/api/activities/<username>', methods=['GET'])
def get_activities(username):
    user = db.users.find_one({'username': username}, {'_id': 1})
    if not user:
        return jsonify({"error": "User not found"}), 404
    print("User ID:", user['_id']) 
    activities = list(db.activities.find({"user": user['_id']}, {'_id': 0,'user':0}))
    print("Activities found:", activities)  
    return jsonify(activities)

# Fetch all sleep data for a user
@app.route('/api/sleep_data/<username>', methods=['GET'])
def get_sleep_data(username):
    # Fetch user ID from the 'users' collection based on username
    user = db.users.find_one({'username': username}, {'_id': 1})
    if not user:
        return jsonify({"error": "User not found"}), 404
    print("User ID:", user['_id'])  # Debug print to check the user ID
    sleep_data = list(db.sleep.find({"user": user['_id']}, {'_id': 0, 'user': 0}))  # Adjust 'user' field as necessary
    print("Sleep data found:", sleep_data)  # Debug print to check sleep data
    return jsonify(sleep_data)


# Fetch all mood scores for a user
@app.route('/api/mood_scores/<username>', methods=['GET'])
def get_mood_scores(username):
    user = db.users.find_one({'username': username}, {'_id': 1})
    if not user:
        return jsonify({"error": "User not found"}), 404
    print("User ID:", user['_id'])  # Debug print to check the user ID
    mood_scores = list(db.mood_score.find({"user": user['_id']}, {'_id': 0, 'user': 0}))  # Adjust 'user' field as necessary
    print("Mood scores found:", mood_scores)  # Debug print to check mood scores
    return jsonify(mood_scores)


if __name__ == '__main__':
    app.run(debug=True)
