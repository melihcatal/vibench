import os
from google.cloud import translate_v3
from google.cloud import texttospeech_v1
from google.cloud import aiplatform

def get_translation_client():
    """Provides a configured Google Cloud Translation client."""
    return translate_v3.TranslationServiceClient()

def get_text_to_speech_client():
    """Provides a configured Google Cloud Text-to-Speech client."""
    return texttospeech_v1.TextToSpeechClient()

def get_vertex_ai_prediction_client(api_endpoint: str = "us-central1-aiplatform.googleapis.com"):
    """Provides a configured Google Cloud Vertex AI Prediction client."""
    return aiplatform.gapic.PredictionServiceClient(client_options={"api_endpoint": api_endpoint})

