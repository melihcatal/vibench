import os
from google.cloud import firestore

db = firestore.client()

def get_client():
    return db