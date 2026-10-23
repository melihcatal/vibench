import os
from google.cloud import logging
import google.generativeai as genai
import requests
from google.cloud import translate_v2 as translate

class ObservabilityClient:
    """
    Provides initialized clients for various observability and AI services.
    """
    def __init__(self):
        # Google Cloud Logging Client
        self._logging_client = None

        # Gemini API Client for LLM Inference and Embeddings
        self._gemini_initialized = False
        self._gemini_api_key = os.getenv("GOOGLE_API_KEY")

        # Perspective API for Text Content Safety
        self._perspective_api_key = os.getenv("PERSPECTIVE_API_KEY")
        self._perspective_api_base_url = "https://commentanalyzer.googleapis.com/v1alpha1"

        # Google Cloud Translation Client
        self._translate_client = None

    def get_logging_client(self):
        if self._logging_client is None:
            self._logging_client = logging.Client()
        return self._logging_client

    def get_gemini_model(self, model_name: str = "gemini-pro"):
        if not self._gemini_initialized:
            if not self._gemini_api_key:
                raise ValueError("GOOGLE_API_KEY environment variable not set for Gemini API.")
            genai.configure(api_key=self._gemini_api_key)
            self._gemini_initialized = True
        return genai.GenerativeModel(model_name)

    def get_gemini_embedding_model(self, model_name: str = "models/embedding-001"):
        if not self._gemini_initialized:
            if not self._gemini_api_key:
                raise ValueError("GOOGLE_API_KEY environment variable not set for Gemini API.")
            genai.configure(api_key=self._gemini_api_key)
            self._gemini_initialized = True
        return model_name # The embedding function takes the model name directly

    def get_perspective_api_config(self):
        if not self._perspective_api_key:
            raise ValueError("PERSPECTIVE_API_KEY environment variable not set for Perspective API.")
        return {
            "api_key": self._perspective_api_key,
            "base_url": self._perspective_api_base_url
        }

    def get_translate_client(self):
        if self._translate_client is None:
            self._translate_client = translate.Client()
        return self._translate_client

observability_client = ObservabilityClient()
