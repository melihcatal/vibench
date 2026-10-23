from pymongo import MongoClient

def store_note(note):
    client = MongoClient(os.getenv('MONGODB_URI'))
    db = client.onboarding
    notes_collection = db.notes
    notes_collection.insert_one(note)