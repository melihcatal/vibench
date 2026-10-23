from pymongo import MongoClient

client = MongoClient('YOUR_MONGODB_ATLAS_URI')
db = client.onboarding
collection = db.notes

def store_note(user_id, note):
    collection.insert_one({'user_id': user_id, 'note': note})