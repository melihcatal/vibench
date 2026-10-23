import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth
from google.cloud import translate_v2 as translate
from google.cloud import firestore
from google.cloud import aiplatform
import requests

class IdentityClientConfig:
    def __init__(self):
        self.firebase_api_key = os.environ.get("FIREBASE_API_KEY")
        self.firebase_project_id = os.environ.get("FIREBASE_PROJECT_ID")
        self.firebase_credentials_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
        self.gcp_project_id = os.environ.get("GCP_PROJECT_ID")
        self.gcp_location = os.environ.get("GCP_LOCATION", "us-central1")

        if not self.firebase_api_key:
            raise ValueError("FIREBASE_API_KEY environment variable not set.")
        if not self.firebase_project_id:
            raise ValueError("FIREBASE_PROJECT_ID environment variable not set.")
        if not self.gcp_project_id:
            raise ValueError("GCP_PROJECT_ID environment variable not set.")

        if not firebase_admin._apps:
            if self.firebase_credentials_path:
                cred = credentials.Certificate(self.firebase_credentials_path)
            else:
                cred = credentials.ApplicationDefault()
            firebase_admin.initialize_app(cred, {'projectId': self.firebase_project_id})

        self._auth_client = None
        self._translate_client = None
        self._firestore_client = None
        self._vertex_ai_initialized = False

    @property
    def auth_client(self):
        if self._auth_client is None:
            self._auth_client = auth
        return self._auth_client

    @property
    def translate_client(self):
        if self._translate_client is None:
            self._translate_client = translate.Client(project=self.gcp_project_id)
        return self._translate_client

    @property
    def firestore_client(self):
        if self._firestore_client is None:
            self._firestore_client = firestore.Client(project=self.gcp_project_id)
        return self._firestore_client

    def initialize_vertex_ai(self):
        if not self._vertex_ai_initialized:
            aiplatform.init(project=self.gcp_project_id, location=self.gcp_location)
            self._vertex_ai_initialized = True

config = IdentityClientConfig()
