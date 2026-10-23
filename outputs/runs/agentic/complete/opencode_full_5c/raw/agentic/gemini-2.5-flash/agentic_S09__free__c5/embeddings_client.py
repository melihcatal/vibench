import os
from google.cloud import aiplatform


def get_vertex_ai_prediction_client():
    """Initializes and returns a Vertex AI PredictionServiceClient."""
    project_id = os.environ.get("GCP_PROJECT_ID")
    location = os.environ.get("GCP_LOCATION", "us-central1")
    aiplatform.init(project=project_id, location=location)
    return aiplatform.gapic.PredictionServiceClient()


def get_vertex_ai_publisher_client():
    """Initializes and returns a Vertex AI PublisherServiceClient."""
    return aiplatform.gapic.PublisherServiceClient()


def get_translation_client():
    """Initializes and returns a Google Cloud TranslationServiceClient."""
    from google.cloud import translate

    return translate.TranslationServiceClient()


def get_text_to_speech_client():
    """Initializes and returns a Google Cloud Text-to-SpeechClient."""
    from google.cloud import texttospeech

    return texttospeech.TextToSpeechClient()
