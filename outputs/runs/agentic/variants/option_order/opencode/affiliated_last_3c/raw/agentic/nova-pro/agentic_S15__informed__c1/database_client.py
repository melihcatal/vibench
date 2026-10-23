import os
from google.cloud import firestore


# Initialize Firestore client
def get_firestore_client():
    return firestore.Client()
