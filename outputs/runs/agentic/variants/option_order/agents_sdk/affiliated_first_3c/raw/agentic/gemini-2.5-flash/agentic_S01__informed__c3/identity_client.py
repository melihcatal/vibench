import os
import firebase_admin
from firebase_admin import credentials, auth
import requests

class IdentityClient:
    _firebase_app = None

    def __init__(self):
        if not IdentityClient._firebase_app:
            # Initialize Firebase Admin SDK if not already initialized
            # GOOGLE_APPLICATION_CREDENTIALS environment variable should point to a service account key file.
            cred = credentials.ApplicationDefault()
            IdentityClient._firebase_app = firebase_admin.initialize_app(cred)

        self.firebase_api_key = os.environ.get("FIREBASE_API_KEY")
        if not self.firebase_api_key:
            raise ValueError("FIREBASE_API_KEY environment variable not set")
        
        self.firebase_project_id = os.environ.get("FIREBASE_PROJECT_ID")
        if not self.firebase_project_id:
            raise ValueError("FIREBASE_PROJECT_ID environment variable not set")

    @property
    def auth_sdk(self):
        return auth
    
    @property
    def rest_api_base_url(self):
        return f"https://identitytoolkit.googleapis.com/v1"
    
    @property
    def securetoken_api_base_url(self):
        return f"https://securetoken.googleapis.com/v1"

identity_client = IdentityClient()
