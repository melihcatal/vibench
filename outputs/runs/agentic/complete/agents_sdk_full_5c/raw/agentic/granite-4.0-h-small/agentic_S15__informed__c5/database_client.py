import os
from google.cloud import firestore

class NoSQLClient:
    """
    Thin wrapper around Google Firestore client for managed NoSQL operations.
    """
    def __init__(self, service: str = 'Firestore'):
        if service.lower() != 'firestore':
            raise NotImplementedError(f"Service {service} not supported in this demo.")
        # Ensure credentials are loaded from env var GOOGLE_APPLICATION_CREDENTIALS
        self.client = firestore.Client()
