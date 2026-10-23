import os
from pymongo import MongoClient

client = MongoClient(os.getenv('MONGODB_ATLAS_URI'))
db = client.onboarding
notes_collection = db.notes

def store_note(user_id, note):
    note_doc = {
        'user_id': user_id,
        'note': note
    }
    notes_collection.insert_one(note_doc)