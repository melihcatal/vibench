import os
import boto3
from google.cloud import speech
from deepgram import DeepgramClient


def get_aws_transcribe_client(region_name=None):
    """
    Returns an AWS Transcribe client.
    """
    region = region_name or os.environ.get("AWS_REGION", "us-east-1")
    return boto3.client("transcribe", region_name=region)


def get_google_speech_client():
    """
    Returns a Google Cloud Speech-to-Text client.
    """
    # Assumes GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    # or gcloud CLI is authenticated.
    return speech.SpeechClient()


def get_assemblyai_api_key():
    """
    Returns the AssemblyAI API key from environment variables.
    """
    api_key = os.environ.get("ASSEMBLYAI_API_KEY")
    if not api_key:
        raise ValueError("ASSEMBLYAI_API_KEY environment variable not set.")
    return api_key


def get_deepgram_client():
    """
    Returns a Deepgram client.
    """
    api_key = os.environ.get("DEEPGRAM_API_KEY")
    if not api_key:
        raise ValueError("DEEPGRAM_API_KEY environment variable not set.")
    return DeepgramClient(api_key)


def get_openai_api_key():
    """
    Returns the OpenAI API key from environment variables.
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")
    return api_key


def get_cohere_api_key():
    """
    Returns the Cohere API key from environment variables.
    """
    api_key = os.environ.get("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY environment variable not set.")
    return api_key


def get_aws_comprehend_client(region_name=None):
    """
    Returns an AWS Comprehend client.
    """
    region = region_name or os.environ.get("AWS_REGION", "us-east-1")
    return boto3.client("comprehend", region_name=region)


def get_google_translate_client():
    """
    Returns a Google Cloud Translation client.
    """
    from google.cloud import translate
    return translate.TranslationServiceClient()

