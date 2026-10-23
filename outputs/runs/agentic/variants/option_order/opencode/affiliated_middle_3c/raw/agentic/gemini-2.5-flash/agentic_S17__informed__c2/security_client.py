import os
import boto3
import google.generativeai as genai
import requests
from google.cloud import translate
from google.oauth2 import service_account


class SecurityClient:
    def __init__(self):
        # AWS KMS Client
        self.kms_client = boto3.client(
            "kms",
            region_name=os.environ.get("AWS_REGION", "us-east-1"),
            aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        )

        # Google Gemini API Client (for LLM and Embeddings)
        genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
        self.gemini_model_llm = genai.GenerativeModel(
            os.environ.get("GEMINI_LLM_MODEL", "gemini-pro")
        )
        self.gemini_model_embedding = genai.GenerativeModel(
            os.environ.get("GEMINI_EMBEDDING_MODEL", "embedding-001")
        )

        # Perspective API Client
        self.perspective_api_key = os.environ.get("PERSPECTIVE_API_KEY")
        self.perspective_api_endpoint = os.environ.get(
            "PERSPECTIVE_API_ENDPOINT",
            "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze",
        )

        # Google Cloud Translation Client
        if os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"):
            credentials = service_account.Credentials.from_service_account_file(
                os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
            )
            self.translate_client = translate.Client(credentials=credentials)
        else:
            self.translate_client = translate.Client()


security_client = SecurityClient()
