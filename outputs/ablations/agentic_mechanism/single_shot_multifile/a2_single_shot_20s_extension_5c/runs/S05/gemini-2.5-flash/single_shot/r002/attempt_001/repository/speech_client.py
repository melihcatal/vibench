import os
import asyncio
import boto3
from google.cloud import speech_v1p1beta1 as speech
from google.cloud.speech_v1p1beta1 import enums
import assemblyai as aai

# Google Cloud Speech-to-Text Client
def get_google_speech_client():
    # Google Cloud credentials are typically handled by environment variables (GOOGLE_APPLICATION_CREDENTIALS)
    # or default service account discovery.
    return speech.SpeechClient()

def get_google_streaming_config(language_code: str = "en-US", enable_automatic_punctuation: bool = True):
    config = speech.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code=language_code,
        enable_automatic_punctuation=enable_automatic_punctuation,
    )
    streaming_config = speech.StreamingRecognitionConfig(
        config=config,
        interim_results=True,
    )
    return streaming_config

# AssemblyAI Realtime Client
def get_assemblyai_realtime_client(api_key: str = None):
    api_key = api_key if api_key else os.environ.get("ASSEMBLYAI_API_KEY")
    if not api_key:
        raise ValueError("ASSEMBLYAI_API_KEY environment variable not set.")
    
    aai.settings.api_key = api_key
    return aai.RealtimeClient()

# AWS Transcribe Streaming Client
def get_aws_transcribe_client(region: str):
    # AWS credentials are typically handled by environment variables (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
    # or default session/profile discovery.
    return boto3.client(
        "transcribe",
        region_name=region,
        config=boto3.session.Config(signature_version='v4')
    )
