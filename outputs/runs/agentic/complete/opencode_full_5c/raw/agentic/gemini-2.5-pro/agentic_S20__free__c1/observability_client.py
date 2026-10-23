import os
import google.generativeai as genai
from google.cloud import logging_v2
from google.cloud import translate_v2 as translate
from googleapiclient import discovery


def get_logging_client():
    """Initializes and returns a Google Cloud Logging client."""
    return logging_v2.LoggingServiceV2Client()


def get_project_id():
    """Returns the Google Cloud project ID from environment variables."""
    return os.environ.get("GOOGLE_CLOUD_PROJECT")


def get_generative_model_client(model_name="gemini-1.5-flash"):
    """Initializes and returns a Google Generative AI model client."""
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable not set.")
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(model_name)
    return model


def get_perspective_client():
    """Initializes and returns a Perspective API client."""
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")
    return discovery.build(
        "commentanalyzer",
        "v1alpha1",
        developerKey=api_key,
        static_discovery=False,
    )


def get_translate_client():
    """Initializes and returns a Google Cloud Translate client."""
    return translate.Client()
