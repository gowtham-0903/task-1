from pymongo import MongoClient
import json
from bson import ObjectId
from datetime import datetime

# Custom JSON encoder to handle ObjectId and datetime
class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)  # Convert ObjectId to string
        if isinstance(o, datetime):
            return o.isoformat()  # Convert datetime to ISO string format
        return super().default(o)

# MongoDB Connection
client = MongoClient("mongodb://localhost:27017/")
db = client['wysa']
combined_data_collection = db['combined_data']

# Fetch and limit to first 5 records from combined_data collection
sample_data = list(combined_data_collection.find().limit(5))

# Save to a JSON file using the custom encoder
with open('combined_data_output.json', 'w') as file:
    json.dump(sample_data, file, indent=4, cls=JSONEncoder)  # Ensure cls=JSONEncoder is used

print("Data has been saved to combined_data_output.json")
