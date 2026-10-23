import os
from pymongo import MongoClient

# Configuration
mongodb_atlas_uri = os.getenv('MONGODB_ATLAS_URI')

# Profile Note Store
def profile_note_store(user_id, note):
    client = MongoClient(mongodb_atlas_uri)
    db = client.onboarding
    notes = db.notes
    notes.update_one({'user_id': user_id}, {'$set': {'note': note}}, upsert=True)