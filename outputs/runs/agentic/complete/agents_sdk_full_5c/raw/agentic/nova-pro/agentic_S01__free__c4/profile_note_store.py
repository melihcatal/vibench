from pymongo import MongoClient

def store_note(user_id, note):
    client = MongoClient(os.getenv('MONGODB_URI'))
    db = client.onboarding
    notes = db.notes
    notes.update_one({'user_id': user_id}, {'$set': {'note': note}}, upsert=True)