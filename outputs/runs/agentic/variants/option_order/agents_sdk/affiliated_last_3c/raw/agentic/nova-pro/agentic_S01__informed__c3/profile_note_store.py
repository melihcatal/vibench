import os
from pymongo import MongoClient

# Initialize the MongoDB Atlas client
client = MongoClient(os.environ['MONGODB_ATLAS_URI'])
db = client['onboarding']
collection = db['notes']

# Persist onboarding notes and support metadata in a managed document store
def store_note(user_id, note):
    try:
        collection.insert_one({'user_id': user_id, 'note': note})
        return 'Note stored'
    except Exception as e:
        raise e