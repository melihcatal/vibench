import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety import ContentSafetyClient
from openai import OpenAI
from google.cloud import translate_v2 as translate
from azure.cognitiveservices.speech import SpeechConfig, SpeechSynthesizer

def get_azure_content_safety_client():
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")
    if not endpoint or not key:
        raise ValueError("AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY must be set.")
    return ContentSafetyClient(endpoint, AzureKeyCredential(key))

def get_openai_client():
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY must be set.")
    return OpenAI(api_key=api_key)

def get_google_translate_client():
    return translate.Client()

def get_azure_speech_synthesizer():
    speech_key = os.environ.get("AZURE_SPEECH_KEY")
    speech_region = os.environ.get("AZURE_SPEECH_REGION")
    if not speech_key or not speech_region:
        raise ValueError("AZURE_SPEECH_KEY and AZURE_SPEECH_REGION must be set.")
    speech_config = SpeechConfig(subscription=speech_key, region=speech_region)
    speech_config.speech_synthesis_voice_name = os.environ.get("AZURE_SPEECH_VOICE_NAME", "en-US-JennyNeural")
    return SpeechSynthesizer(speech_config=speech_config, audio_config=None)
