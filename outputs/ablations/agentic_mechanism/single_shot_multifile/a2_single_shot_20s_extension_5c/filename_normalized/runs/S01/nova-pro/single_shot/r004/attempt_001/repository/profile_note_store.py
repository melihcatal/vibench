import os
from pymongo import MongoClient

def store_profile_note(note):
    client = MongoClient(os.getenv('MONGODB_URI'))
    db = client.onboarding
    notes = db.notes
    notes.insert_one(note)
