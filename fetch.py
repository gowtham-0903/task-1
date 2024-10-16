import json
from pymongo import MongoClient
from datetime import datetime

def extract_data(collection, date):
    pipeline = [
        {
            '$match': {
                'DATE': date
            }
        },
        {
            '$group': {
                '_id': '$USER',
                'mood_score': {'$avg': '$SLEEP SCORE'},
                'activities': {'$push': '$Activity'},
                'sleep_hours': {'$sum': {'$hour': {'$subtract': ['$HOURS OF_SLEEP', '00:00:00']}}}
            }
        }
    ]
    return list(collection.aggregate(pipeline))

def transform_data(data):
    return data  # Here you can add any additional transformations if needed

def load_data_to_json(data, file_path):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

def main():
    client = MongoClient('mongodb://localhost:27017/')  # Adjust your connection string accordingly
    db = client['wysa']
    collection = db['combined_data']
    
    target_date = datetime(2022, 4, 1)  # Set your desired date
    raw_data = extract_data(collection, target_date)
    transformed_data = transform_data(raw_data)
    
    load_data_to_json(transformed_data, 'output.json')
    print("Data has been saved to output.json")

if __name__ == "__main__":
    main()
