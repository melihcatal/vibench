import os
import json
from typing import Dict, List
import requests
from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

# Load credentials
API_KEY = os.getenv("IBM_TTS_APIKEY")
SERVICE_URL = os.getenv("IBM_TTS_URL")
assert API_KEY and SERVICE_URL, "Set IBM_TTS_APIKEY and IBM_TTS_URL"

authenticator = IAMAuthenticator(API_KEY)
client = TextToSpeechV1(authenticator=authenticator)
client.set_service_url(SERVICE_URL)


def get_audio_bytes(text: str, voice: str = "en-US_MichaelV3Voice") -> bytes:
    """Synthesize plain text and return raw audio bytes."""
    result = client.synthesize(text, voice, accept="audio/wav")
    return result.content


def get_ssml_audio_bytes(ssml: str, voice: str = "en-US_MichaelV3Voice") -> bytes:
    """Synthesize SSML and return raw audio bytes."""
    result = client.synthesize_using_ssml(ssml, voice, accept="audio/wav")
    return result.content


# Voice catalog helper (optional)
def list_voices() -> List[Dict]:
    resp = client.list_voices()
    return resp.result["voices"]
