from pymongo import MongoClient

def store_note(note):
    client = MongoClient('YOUR_MONGODB_URI')
    db = client['onboarding']
    collection = db['notes']
    collection.insert_one(note)