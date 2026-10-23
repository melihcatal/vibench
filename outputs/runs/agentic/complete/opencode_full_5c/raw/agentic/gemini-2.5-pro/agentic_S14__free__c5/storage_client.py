import os
from google.cloud import storage
from google.cloud import vision
from google.cloud import translate_v2 as translate
import openai
import cohere


def get_storage_client() -> storage.Client:
    """Initializes and returns a Google Cloud Storage client."""
    return storage.Client()


def get_vision_client() -> vision.ImageAnnotatorClient:
    """Initializes and returns a Google Cloud Vision client."""
    return vision.ImageAnnotatorClient()


def get_translate_client() -> translate.Client:
    """Initializes and returns a Google Cloud Translate client."""
    return translate.Client()


def get_openai_client() -> openai.OpenAI:
    """Initializes and returns an OpenAI client."""
    api_key = os.environ.get("OPENAI_API_KEY")
    return openai.OpenAI(api_key=api_key)


def get_cohere_client() -> cohere.Client:
    """Initializes and returns a Cohere client."""
    api_key = os.environ.get("COHERE_API_KEY")
    return cohere.Client(api_key)


def get_gcs_bucket_name() -> str:
    """Retrieves the GCS bucket name from environment variables."""
    bucket_name = os.environ.get("GCS_BUCKET_NAME")
    if not bucket_name:
        raise ValueError("GCS_BUCKET_NAME environment variable not set.")
    return bucket_name
