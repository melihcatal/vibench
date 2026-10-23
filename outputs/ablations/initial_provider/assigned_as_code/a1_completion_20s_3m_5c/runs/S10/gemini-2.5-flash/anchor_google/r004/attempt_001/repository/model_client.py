import os
from google import genai
from google.cloud import aiplatform
from google.cloud import translate_v3 as translate
from google.cloud import texttospeech


def get_gemini_client(api_key=None):
    api_key = api_key or os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY not found in environment variables or config.")
    return genai.Client(api_key=api_key)


def get_vertex_ai_prediction_client(project_id=None, location=None):
    project_id = project_id or os.environ.get("GOOGLE_CLOUD_PROJECT")
    location = location or os.environ.get("GOOGLE_CLOUD_REGION")
    if not project_id or not location:
        raise ValueError("GOOGLE_CLOUD_PROJECT and GOOGLE_CLOUD_REGION must be set for Vertex AI.")
    return aiplatform.gapic.PredictionServiceClient(client_options={"api_endpoint": f"{location}-aiplatform.googleapis.com"})

def get_translate_client(project_id=None):
    project_id = project_id or os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT must be set for Translation API.")
    return translate.TranslationServiceClient()

def get_text_to_speech_client():
    return texttospeech.TextToSpeechClient()
