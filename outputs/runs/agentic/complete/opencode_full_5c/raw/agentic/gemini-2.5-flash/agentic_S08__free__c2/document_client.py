from google.cloud import documentai_v1beta3 as documentai
import os


def get_documentai_client():
    """
    Provides a configured Google Cloud Document AI client.
    """
    return documentai.DocumentProcessorServiceClient()


def get_processor_path(project_id: str, location: str, processor_id: str) -> str:
    """
    Constructs the full processor path for Google Cloud Document AI.
    """
    client = get_documentai_client()
    return client.processor_path(project_id, location, processor_id)


def get_gemini_model():
    """
    Configures and returns a Google Gemini generative model.
    """
    import google.generativeai as genai

    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    return genai.GenerativeModel("gemini-pro")


def get_logging_client():
    """
    Provides a configured Google Cloud Logging client.
    """
    from google.cloud import logging

    return logging.Client()


def get_translation_client():
    """
    Provides a configured Google Cloud Translation client.
    """
    from google.cloud import translate_v3 as translate

    return translate.TranslationServiceClient()


def get_firestore_client():
    """
    Provides a configured Google Cloud Firestore client.
    """
    from google.cloud import firestore

    return firestore.Client()


def get_vertex_ai_client():
    """
    Initializes and returns a Vertex AI client for content moderation.
    """
    from google.cloud import aiplatform

    # Initialize Vertex AI with your project and location
    # aiplatform.init(project=os.environ.get("GOOGLE_CLOUD_PROJECT"), location=os.environ.get("GOOGLE_CLOUD_LOCATION"))
    # For this example, we might not need a direct client object to call safety features through model directly
    # but we keep this function for consistency if a dedicated client becomes relevant.
    return None  # Or initialize specific Vertex AI components if needed
