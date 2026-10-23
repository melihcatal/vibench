import os
from google.cloud import speech_v1 as speech
from azure.cognitiveservices.speech import SpeechConfig, AudioConfig
from ibm_watson import SpeechToTextV1
import deepgram

# Local configuration and client helper utilities for Streaming Speech-to-Text.
# Provider identifiers are set via environment variables or constants.

# ---- Google Cloud Speech ----
# env: GOOGLE_APPLICATION_CREDENTIALS
# service: Cloud Speech streaming
# sdk: google-cloud-speech
GOOGLE_CLIENT = None

# ---- Azure Speech ----
# env: AZURE_SPEECH_KEY, AZURE_SPEECH_REGION
# service: Azure AI Speech streaming
# sdk: azure-cognitiveservices-speech
AZURE_SPEECH_CONFIG = None

# ---- IBM Watson STT ----
# env: IBM_STT_APIKEY, IBM_STT_URL
# service: Watson Speech to Text WebSocket
# sdk: ibm-watson
WATSON_CLIENT = None

# ---- Deepgram ----
# env: DEEPGRAM_API_KEY
# service: Deepgram Streaming API
# sdk: deepgram-sdk
DEEPGRAM_CLIENT = None

# ---- Amazon Transcribe ----
# env: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION
# service: Amazon Transcribe Streaming
# sdk: boto3
TRANScribe_CLIENT = None


def get_google_client():
    global GOOGLE_CLIENT
    if GOOGLE_CLIENT is None:
        GOOGLE_CLIENT = speech.v1.SpeechClient()
    return GOOGLE_CLIENT


def get_azure_speech_config():
    global AZURE_SPEECH_CONFIG
    if AZURE_SPEECH_CONFIG is None:
        key = os.getenv("AZURE_SPEECH_KEY")
        region = os.getenv("AZURE_SPEECH_REGION")
        AZURE_SPEECH_CONFIG = SpeechConfig(subscription=key, region=region)
    return AZURE_SPEECH_CONFIG


def get_watson_client():
    global WATSON_CLIENT
    if WATSON_CLIENT is None:
        apikey = os.getenv("IBM_STT_APIKEY")
        url = os.getenv("IBM_STT_URL")
        WATSON_CLIENT = SpeechToTextV1(apikey=apikey, url=url)
    return WATSON_CLIENT


def get_deepgram_client():
    global DEEPGRAM_CLIENT
    if DEEPGRAM_CLIENT is None:
        api_key = os.getenv("DEEPGRAM_API_KEY")
        DEEPGRAM_CLIENT = deepgram.setup_api(
            base_url="https://api.deepgram.com", api_key=api_key
        )
    return DEEPGRAM_CLIENT


def get_transcribe_client():
    global TRANScribe_CLIENT
    if TRANScribe_CLIENT is None:
        TRANScribe_CLIENT = speech_v1.SpeechClient()  # placeholder for boto3 usage
    return TRANScribe_CLIENT
