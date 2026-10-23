import os
from pymongo import MongoClient


def get_mongo_client():
    uri = os.getenv("MONGODB_URI")
    if not uri:
        raise ValueError("MONGODB_URI environment variable not set")
    return MongoClient(uri)


def get_database(client):
    return client["app_db"]


def get_documents_collection(db):
    return db["documents"]
