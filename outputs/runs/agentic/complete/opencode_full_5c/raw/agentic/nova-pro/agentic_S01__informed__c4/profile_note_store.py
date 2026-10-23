from pymongo import MongoClient


def profile_note_store(note):
    client = MongoClient("YOUR_MONGODB_ATLAS_URI")
    db = client.onboarding
    notes = db.notes
    notes.insert_one(note)
    return "Note stored successfully"
