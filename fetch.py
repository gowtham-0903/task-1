import csv
import pymongo
from bson import ObjectId
from datetime import datetime

# MongoDB setup
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["health_db"]

class DataLoader:
    @staticmethod
    def load_users_activity(file_path):
        # Set to track unique users
        unique_users = set()

        with open(file_path, 'r') as file:
            reader = csv.reader(file)
            header = next(reader)  # Skip the header

            for row in reader:
                user_id = row[0]  # Assuming first column is the username
                unique_users.add(user_id)

                # Insert activity data
                activity_data = {
                    "user": DataLoader.get_user_id(user_id),  # Fetches or creates user
                    "date": datetime.strptime(row[1], '%m/%d/%y'),  # Date field
                    "startTime": row[2],
                    "endTime": row[3],
                    "activity": row[5],
                    "logType": row[6],
                    "steps": int(row[7]),
                    "distance": float(row[8]) if row[8] else 0,
                    "elevationGain": float(row[9]) if row[9] else 0,
                    "calories": int(row[10]) if row[10] else 0
                }
                db.activities.insert_one(activity_data)

        # Load unique users to the users collection
        for user in unique_users:
            DataLoader.insert_user(user)

    @staticmethod
    def insert_user(user):
        user_data = {
            "username": user,
            "timezone": "Americas/Los Angeles",
            "version": 70,
            "app": "Wysa",
            "country": "US"
        }
        db.users.update_one({"username": user}, {"$set": user_data}, upsert=True)

    @staticmethod
    def get_user_id(username):
        user = db.users.find_one({"username": username})
        if user:
            return user["_id"]
        else:
            return db.users.insert_one({"username": username}).inserted_id
    
        
    @staticmethod
    def load_sleep_data(file_path):
        with open(file_path, 'r') as file:
            reader = csv.reader(file)
            header = next(reader)  # Skip the header

            for row in reader:
                user_id = row[0]  # Assuming first column is the username

                sleep_data = {
                    "user": DataLoader.get_user_id(user_id),  # Fetches or creates user
                    "date": datetime.strptime(row[2], '%m/%d/%y'),  # Date field
                    "sleepScore": int(row[3]),
                    "hoursOfSleep": row[4],
                    "remSleep": row[5],
                    "deepSleep": row[6],
                    "heartRateBelowResting": row[7],
                    "durationInBed": row[8]
                }
                db.sleep.insert_one(sleep_data)

    @staticmethod
    def get_user_id(username):
        user = db.users.find_one({"username": username})
        if user:
            return user["_id"]
        else:
            return db.users.insert_one({"username": username}).inserted_id
    
    
    @staticmethod
    def upload_mood_score(username, mood_value, created_at):
        user_id = DataLoader.get_user_id(username)
        mood_score_data = {
            "user": user_id,
            "field": "mood score",
            "value": mood_value,
            "createdAt": created_at,
            "updatedAt": created_at
        }
        db.mood_score.insert_one(mood_score_data)

# Load user activity
DataLoader.load_users_activity("activity_data.csv")

# Load sleep data
DataLoader.load_sleep_data("sleep_data.csv")

# Upload mood score example
DataLoader.upload_mood_score("A", 8, datetime.utcnow())
