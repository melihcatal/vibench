import os
from google.cloud import kms_v1
import boto3
import requests


class SecurityClient:
    """Provides client utilities and configuration for various security services."""

    def __init__(self):
        # Google Cloud KMS Configuration
        self.gcp_project_id = os.getenv("GCP_PROJECT_ID")
        self.gcp_location_id = os.getenv("GCP_KMS_LOCATION_ID")
        self.gcp_key_ring_id = os.getenv("GCP_KMS_KEY_RING_ID")
        self.gcp_key_id = os.getenv("GCP_KMS_KEY_ID")
        self.gcp_key_version_id = os.getenv("GCP_KMS_KEY_VERSION_ID")
        self._gcp_kms_client = None

        # AWS KMS Configuration
        self.aws_region = os.getenv("AWS_REGION", "us-east-1")
        self._aws_kms_client = None

        # Azure AI Content Safety Configuration
        self.azure_content_safety_endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
        self.azure_content_safety_key = os.getenv("AZURE_CONTENT_SAFETY_KEY")

        # Google Gemini API (for embeddings) Configuration
        self.google_gemini_api_key = os.getenv("GOOGLE_API_KEY")

        # Google Cloud Translation Configuration
        self.gcp_translation_project_id = os.getenv(
            "GCP_TRANSLATION_PROJECT_ID", self.gcp_project_id
        )
        self._gcp_translation_client = None

    def get_gcp_kms_client(self):
        if self._gcp_kms_client is None:
            self._gcp_kms_client = kms_v1.KeyManagementServiceClient()
        return self._gcp_kms_client

    def get_aws_kms_client(self):
        if self._aws_kms_client is None:
            self._aws_kms_client = boto3.client("kms", region_name=self.aws_region)
        return self._aws_kms_client

    def get_gcp_translation_client(self):
        from google.cloud import translate_v3

        if self._gcp_translation_client is None:
            self._gcp_translation_client = translate_v3.TranslationServiceClient()
        return self._gcp_translation_client
