import os
from openai import OpenAI
from google.cloud import documentai_v1 as documentai
from google.cloud import firestore_v1 as firestore
from google.cloud import translate_v3 as translate
from google.cloud import aiplatform
from anthropic import Anthropic
import cohere


def get_openai_client():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set")
    return OpenAI(api_key=api_key)


def get_documentai_client():
    # Google Cloud credentials are typically handled by the environment or gcloud CLI
    # For service account key file:
    # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/your/key.json"
    return documentai.DocumentProcessorServiceClient()


def get_cohere_client():
    api_key = os.getenv("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY environment variable not set")
    return cohere.Client(api_key)


def get_anthropic_client():
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable not set")
    return Anthropic(api_key=api_key)


def get_content_safety_client():
    # For Google Cloud Content Safety (Vertex AI)
    # Initialize AI Platform, project ID and location might be needed
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    location = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set")
    aiplatform.init(project=project_id, location=location)
    return aiplatform # The client itself is aiplatform for models/services


def get_translate_client():
    return translate.TranslationServiceClient()


def get_firestore_client():
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set")
    return firestore.Client(project=project_id)
