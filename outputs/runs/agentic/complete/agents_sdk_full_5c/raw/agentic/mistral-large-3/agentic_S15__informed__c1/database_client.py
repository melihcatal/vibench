from google.cloud import firestore
import os

def get_firestore_client():
    """
    Initializes and returns a Google Firestore client.
    
    Requires GOOGLE_APPLICATION_CREDENTIALS environment variable for authentication.
    """
    return firestore.Client()