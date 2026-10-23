import os
from google.cloud import logging
import google.generativeai as genai


def get_logging_client():
    # Google Cloud Logging uses GOOGLE_APPLICATION_CREDENTIALS for authentication
    return logging.Client()


def get_gemini_model(model_name: str = "gemini-pro"):
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")
    genai.configure(api_key=api_key)
    return genai.GenerativeModel(model_name)


def get_embedding_model(model_name: str = "models/embedding-001"):
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")
    genai.configure(api_key=api_key)
    return genai.GenerativeModel(model_name)


def get_azure_content_safety_config():
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")
    if not endpoint or not key:
        raise ValueError(
            "AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables must be set."
        )
    return {"endpoint": endpoint, "key": key}
