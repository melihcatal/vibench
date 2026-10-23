import os
from google.cloud import texttospeech
from google.cloud import translate_v3 as translate
from google.cloud import aiplatform
from google.cloud import speech_v1p1beta1 as speech
from google.cloud import storage


def get_tts_client():
    return texttospeech.TextToSpeechClient()


def get_translate_client():
    return translate.TranslationServiceClient()


def get_vertex_ai_client(project_id: str, location: str):
    aiplatform.init(project=project_id, location=location)
    # For embeddings, we will use the PredictionServiceClient directly as aiplatform.init doesn't provide it directly for all models
    # We'll initialize it in script_embedding.py
    return aiplatform  # Initialize SDK for other Vertex AI operations


def get_speech_to_text_client():
    return speech.SpeechClient()


def get_gcs_client():
    return storage.Client()


def get_project_id():
    return os.environ.get("GCP_PROJECT_ID") or os.environ.get("GOOGLE_CLOUD_PROJECT")


def get_gcp_location():
    return os.environ.get("GCP_LOCATION") or "us-central1"
