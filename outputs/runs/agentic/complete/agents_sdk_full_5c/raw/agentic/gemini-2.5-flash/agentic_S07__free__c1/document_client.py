import os
from google.cloud import vision_v1, documentai_v1, translate_v3, language_v1, aiplatform

# Centralized client initialization for Google Cloud services

def get_vision_client() -> vision_v1.ImageAnnotatorClient:
    """Returns a Google Cloud Vision API client."""
    return vision_v1.ImageAnnotatorClient()

def get_documentai_client() -> documentai_v1.DocumentProcessorServiceClient:
    """Returns a Google Cloud Document AI API client."""
    return documentai_v1.DocumentProcessorServiceClient()

def get_translation_client() -> translate_v3.TranslationServiceClient:
    """Returns a Google Cloud Translation API client."""
    return translate_v3.TranslationServiceClient()

def get_vertex_ai_prediction_client() -> aiplatform.PredictionServiceClient:
    """Returns a Google Cloud Vertex AI Prediction Service client."""
    # Ensure Vertex AI project and location are set, typically via env vars or client_options
    # For this example, we assume default project/location or configured via environment variables
    return aiplatform.PredictionServiceClient(client_options={"api_endpoint": f"{os.environ.get("GCP_REGION", "us-central1")}-aiplatform.googleapis.com"})

