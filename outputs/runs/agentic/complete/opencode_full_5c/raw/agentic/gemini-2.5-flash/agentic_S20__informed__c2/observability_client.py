import os
from google.cloud import logging
import google.generativeai as genai
from google.cloud import translate_v2 as translate
import requests


def get_logging_client():
    """Returns a Google Cloud Logging client."""
    return logging.Client()


def get_gemini_model(model_name: str):
    """Returns a Google Gemini model for generative tasks or embeddings."""
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    return genai.GenerativeModel(model_name)


def get_translate_client():
    """Returns a Google Cloud Translation client."""
    return translate.Client()


def get_perspective_api_key():
    """Returns the Perspective API key from environment variables."""
    return os.environ.get("PERSPECTIVE_API_KEY")
