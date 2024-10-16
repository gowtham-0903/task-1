from flask import Flask, jsonify, request
from pymongo import MongoClient

app = Flask(__name__)

# Initialize MongoDB connection
mongo_uri = "mongodb://localhost:27017/"  
client = MongoClient(mongo_uri)
db = client['health_db'] 

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
    print("User ID:", user['_id'])  
    sleep_data = list(db.sleep.find({"user": user['_id']}, {'_id': 0, 'user': 0}))  
    print("Sleep data found:", sleep_data)  
    return jsonify(sleep_data)


# Fetch all mood scores for a user
@app.route('/api/mood_scores/<username>', methods=['GET'])
def get_mood_scores(username):
    user = db.users.find_one({'username': username}, {'_id': 1})
    if not user:
        return jsonify({"error": "User not found"}), 404
    print("User ID:", user['_id'])  
    mood_scores = list(db.mood_score.find({"user": user['_id']}, {'_id': 0, 'user': 0}))  
    print("Mood scores found:", mood_scores)  
    return jsonify(mood_scores)
    
@app.route('/summarised_data/<username>', methods=['GET'])
def get_summarised_data_for_user(username):
    user = db.users.find_one({"username": username}, {'_id': 1, 'username': 1}) 
    if not user:
        return jsonify({"error": "User not found"}), 404
    user_id = user['_id']
    mood_score_data = db.mood_score.find_one({"user": user_id}, sort=[("createdAt", -1)])
    activities_data = list(db.activities.find({"user": user_id}))
    sleep_data = db.sleep_data.find_one({"user": user_id}, sort=[("date", -1)])

    # Create a summarized structure for the user
    user_summary = {
        "user": str(user_id),
        "username": username,
        "date": mood_score_data['createdAt'] if mood_score_data else None,
        "mood_score": mood_score_data['value'] if mood_score_data else None,
        "activity": [
            {
                "activity": activity["activity"],
                "steps": activity["steps"],
                "distance": activity["distance"],
                "duration": activity["endTime"],  
                "calories": activity.get("calories", 0)
            } for activity in activities_data
        ],
        "sleep": {
            "sleep_score": sleep_data["sleepScore"] if sleep_data else None,
            "hours_of_sleep": sleep_data["hoursOfSleep"] if sleep_data else None,
            "duration_in_bed": sleep_data["durationInBed"] if sleep_data else None,
            "deep_sleep": sleep_data["deepSleep"] if sleep_data else None
        }
    }

    # Return the summarized data as JSON
    return jsonify(user_summary)

if __name__ == '__main__':
    app.run(debug=True)
