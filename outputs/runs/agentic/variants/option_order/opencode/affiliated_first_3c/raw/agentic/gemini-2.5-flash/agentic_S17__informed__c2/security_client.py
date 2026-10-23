import os
from google.cloud import kms_v1
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold


class SecurityClient:
    def __init__(self):
        # Google Cloud KMS Client
        self.kms_client = kms_v1.KeyManagementServiceClient()
        self.project_id = os.getenv("GOOGLE_CLOUD_PROJECT", "your-gcp-project-id")
        self.location_id = os.getenv(
            "GOOGLE_CLOUD_KMS_LOCATION", "global"
        )  # Or a specific region like 'us-central1'

        # Gemini API Client for key_usage_summary and compliance_note_translate
        gemini_api_key = os.getenv("GOOGLE_API_KEY")
        if gemini_api_key:
            genai.configure(api_key=gemini_api_key)
            self.gemini_model = genai.GenerativeModel(
                "gemini-pro"
            )  # Or 'gemini-1.5-flash-latest'
        else:
            self.gemini_model = None

        # Perspective API details for payload_safety (will use requests directly in payload_safety.py)
        self.perspective_api_endpoint = (
            "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
        )
        self.perspective_api_key = os.getenv("PERSPECTIVE_API_KEY")

        # Gemini Embeddings Client for crypto_audit_embedding
        if gemini_api_key:
            self.gemini_embedding_model = "models/embedding-001"
        else:
            self.gemini_embedding_model = None

    def get_key_path(self, key_ring_id: str, key_id: str):
        return self.kms_client.crypto_key_path(
            self.project_id, self.location_id, key_ring_id, key_id
        )

    def get_key_version_path(self, key_ring_id: str, key_id: str, key_version_id: str):
        return self.kms_client.crypto_key_version_path(
            self.project_id, self.location_id, key_ring_id, key_id, key_version_id
        )
