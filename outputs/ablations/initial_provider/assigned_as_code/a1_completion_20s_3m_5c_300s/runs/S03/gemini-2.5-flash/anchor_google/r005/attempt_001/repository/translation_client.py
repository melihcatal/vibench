from google.cloud import translate_v3
import os

class TranslationClient:
    def __init__(self, project_id=None, location='global'):
        self.project_id = project_id or os.getenv('GOOGLE_CLOUD_PROJECT')
        if not self.project_id:
            raise ValueError("Google Cloud project ID must be provided or set in GOOGLE_CLOUD_PROJECT environment variable.")
        self.location = location
        self.client = translate_v3.TranslationServiceClient()
        self.parent = f"projects/{self.project_id}/locations/{self.location}"
