import os
from google.cloud import texttospeech
from google.cloud import translate_v3
from google.cloud import language_v1
from google.cloud import speech_v1p1beta1 as speech
import vertexai
from vertexai.preview.language_models import TextEmbeddingModel
import boto3


def get_tts_client():
    return texttospeech.TextToSpeechClient()


def get_translation_client():
    return translate_v3.TranslationServiceClient()


def get_nl_client():
    return language_v1.LanguageServiceClient()


def get_speech_to_text_client():
    return speech.SpeechClient()


def get_vertex_ai_embedding_model():
    # Initialize Vertex AI for the project and location
    # Project ID and location should ideally be configured via environment variables or a config file.
    # For this example, assuming they are set in the environment or hardcoded for brevity.
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT_ID", "your-gcp-project-id")
    location = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")
    vertexai.init(project=project_id, location=location)
    return TextEmbeddingModel.from_pretrained("textembedding-gecko@001")


def get_s3_client():
    # AWS credentials should be configured via environment variables (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
    # or ~/.aws/credentials
    return boto3.client("s3")
