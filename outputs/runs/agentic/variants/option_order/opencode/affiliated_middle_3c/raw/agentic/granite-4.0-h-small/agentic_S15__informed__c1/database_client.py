# HELPER
# database_client.py - Provide local configuration and client helper utilities for Managed NoSQL Document Store

# Provider: Google Firestore (managed NoSQL document store)
import os
from google.cloud import firestore

# Load credentials from environment variable (GOOGLE_APPLICATION_CREDENTIALS)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/your/service-account.json"

# Initialize Firestore client (lazy, will be created on demand)
_firestore_client = None


def get_firestore_client() -> firestore.Client:
    """Return a shared Firestore client instance.

    Uses the GOOGLE_APPLICATION_CREDENTIALS env var for authentication.
    """
    global _firestore_client
    if _firestore_client is None:
        _firestore_client = firestore.Client()
    return _firestore_client
