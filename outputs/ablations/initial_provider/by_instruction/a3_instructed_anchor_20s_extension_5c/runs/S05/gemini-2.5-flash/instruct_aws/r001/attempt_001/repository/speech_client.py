import os
from google.cloud import speech
import boto3

class AWSConfig:
    REGION = os.getenv("AWS_REGION", "us-east-1")
    # In a real application, you'd use AWS credentials for authentication
    # For streaming, a pre-signed URL is typically used, generated server-side.
    # This client is mainly for generating that URL or other AWS interactions.
    # AWS Transcribe Streaming does not directly use a client for the websocket connection itself.

class GoogleCloudConfig:
    # Google Cloud credentials are typically handled by environment variables (GOOGLE_APPLICATION_CREDENTIALS)
    # or by default application credentials when running on GCP infrastructure.
    LANGUAGE_CODE = os.getenv("GOOGLE_CLOUD_SPEECH_LANGUAGE_CODE", "en-US")
    SAMPLE_RATE_HERTZ = 16000
    ENCODING = speech.RecognitionConfig.AudioEncoding.LINEAR16

def get_aws_transcribe_client():
    """Returns a boto3 Transcribe client (for generating pre-signed URLs, etc.)."""
    # Note: For actual streaming, a pre-signed WebSocket URL is used, not a direct client.
    return boto3.client("transcribe", region_name=AWSConfig.REGION)

def get_google_cloud_speech_client():
    """Returns a Google Cloud Speech-to-Text client."""
    return speech.SpeechClient()

# Placeholder for other client helpers if needed
def get_google_cloud_translate_client():
    from google.cloud import translate
    return translate.TranslationServiceClient()

def get_google_cloud_language_client():
    from google.cloud import language_v1
    return language_v1.LanguageServiceClient()

def get_google_cloud_vertex_ai_client():
    # Vertex AI clients can vary. This is a placeholder.
    # from google.cloud import aiplatform
    # aiplatform.init(project=os.getenv("GOOGLE_CLOUD_PROJECT"), location=os.getenv("GOOGLE_CLOUD_REGION"))
    # return aiplatform
    pass # Not directly implemented here to avoid complex init for a helper file
