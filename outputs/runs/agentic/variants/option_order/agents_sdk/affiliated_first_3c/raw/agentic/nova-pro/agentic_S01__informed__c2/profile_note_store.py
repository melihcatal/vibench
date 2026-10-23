import os
from pymongo import MongoClient

def store_note(note):
    client = MongoClient(os.getenv('MONGODB_ATLAS_URI'))
    db = client.onboarding
    collection = db.notes
    result = collection.insert_one(note)
    return result.inserted_id