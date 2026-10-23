import os
import json
from typing import Optional
import requests
from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

# Load credentials (set environment variables before running)
API_KEY = os.getenv("IBM_TTS_APIKEY")
SERVICE_URL = os.getenv("IBM_TTS_URL")
assert API_KEY and SERVICE_URL, (
    "Set IBM_TTS_APIKEY and IBM_TTS_URL environment variables"
)

authenticator = IAMAuthenticator(API_KEY)
tts_service = TextToSpeechV1(authenticator=authenticator)
tts_service.set_service_url(SERVICE_URL)


# Helper to list available voices
def list_voices() -> list:
    response = tts_service.list_voices()
    return response.result["voices"]


# Helper to synthesize plain text
def synthesize_plain(
    text: str, voice: Optional[str] = None, accept: str = "audio/wav"
) -> bytes:
    response = tts_service.synthesize(text, voice, accept)
    return response.content


# Helper to synthesize SSML
def synthesize_ssml(
    ssml: str, voice: Optional[str] = None, accept: str = "audio/wav"
) -> bytes:
    response = tts_service.synthesize_using_ssml(ssml, voice, accept)
    return response.content
