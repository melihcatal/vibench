import os
from pymongo import MongoClient

MONGODB_ATLAS_URI = os.getenv("MONGODB_ATLAS_URI")


def store_note(note):
    client = MongoClient(MONGODB_ATLAS_URI)
    db = client.onboarding
    notes_collection = db.notes
    notes_collection.insert_one(note)
