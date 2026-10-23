import os
from pymongo import MongoClient

# Configuration
MONGODB_ATLAS_URI = os.getenv("MONGODB_ATLAS_URI")

# MongoDB Atlas client
client = MongoClient(MONGODB_ATLAS_URI)
db = client["onboarding"]
collection = db["notes"]


def store_note(note):
    collection.insert_one(note)
