import os
from google.cloud import logging
import google.generativeai as genai
from google.cloud import translate_v2 as translate
import requests


class ObservabilityClient:
    def __init__(self):
        # Google Cloud Logging
        self.logging_client = logging.Client()
        self.log_name = os.getenv("GOOGLE_CLOUD_LOG_NAME", "my-application-log")

        # Google Gemini API for LLM and Embeddings
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        self.gemini_model = os.getenv("GEMINI_MODEL_ID", "gemini-pro")
        self.gemini_embedding_model = os.getenv(
            "GEMINI_EMBEDDING_MODEL_ID", "models/embedding-001"
        )

        # Perspective API for Content Safety
        self.perspective_api_key = os.getenv("PERSPECTIVE_API_KEY")
        self.perspective_api_endpoint = (
            "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
        )

        # Google Cloud Translation
        self.translate_client = translate.Client()
