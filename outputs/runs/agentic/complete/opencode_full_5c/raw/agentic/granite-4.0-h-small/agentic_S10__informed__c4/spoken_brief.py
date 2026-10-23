import os
import json
from model_client import get_provider_config, normalize_response
from model_models import PromptRequest, PromptResponse

# Choose a TTS service (set env var TTS_PROVIDER, default: dashscope)
TTS_PROVIDER = os.getenv("TTS_PROVIDER", "dashscope")

async def generate_spoken_brief(text: str) -> bytes:
    """Create an audio file (bytes) that reads out `text` using the hosted TTS service.
    Returns the raw audio data as bytes.
    """
    config = get_provider_config(TTS_PROVIDER)
    client = get_tts_client(TTS_PROVIDER)

    # Build provider‑specific request payload
    payload = {
        "text": text,
        "voice": "default",  # optional: many services accept a voice ID
    }

    raw_resp = await client.synthesize_speech(payload)
    # Services usually return an audio stream or base64‑encoded blob.
    # Here we assume the response has a `.audio_content` attribute (bytes).
    if hasattr(raw_resp, "audio_content"):
        return raw_resp.audio_content
    elif "audio_content" in raw_resp:
        return raw_resp["audio_content"]
    else:
        raise ValueError(f"Unexpected TTS response format: {raw_resp}")

# Provider‑specific async TTS client definitions
# def get_tts_client(provider: str) -> Any:
#     if provider == "dashscope":
#         import dashscope
#         client = dashscope.AsyncClient(api_key=os.getenv("DASHSCOPE_API_KEY"))
#         return client.synthesize_speech
#     elif provider == "elevenlabs":
#         import elevenlabs
#         client = elevenlabs.Client(api_key=os.getenv("ELEVENLABS_API_KEY"))
#         # elevenlabs returns a URL; we fetch the bytes
def fetch_audio(url: str) -> bytes:
#             import requests
#             r = requests.get(url)
#             return r.content
#         return fetch_audio(client.synthesize({"input": text})["url"])
#     elif provider == "polly":
#         import boto3
#         client = boto3.client('polly', region_name='us-east-1')
#         resp = client.synthesize_speech(Text=text, OutputFormat='mp3', VoiceId='Joanna')
#         return resp['AudioStream'].read()
#     elif provider == "google":
#         from google.cloud import texttospeech
#         client = texttospeech.TextToSpeechClient()
#         synthesis = client.synthesize_speech(input_speech=texttospeech.SynthesisInput(text=text),
#                                                voice=texttospeech.Voice(selection=texttospeech.VoiceSelectionParams(language_code='en-US', name='en-US-Wavenet-D')),
#                                                audio_config=texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3))
#         return synthesis.audio_content
#     elif provider == "watson":
#         from ibm_watson import TextToSpeechV1
#         from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
#         authenticator = IAMAuthenticator(os.getenv("IBM_TTS_APIKEY"))
#         client = TextToSpeechV1(authenticator=authenticator)
#         client.set_service_url(os.getenv("IBM_TTS_URL"))
#         response = client.synthesize(text=text, voice='en-US_MichaelV3Voice', accept='audio/mp3')
#         return response.get_result().content
#     elif provider == "azure":
#         from azure.cognitiveservices.speech import SpeechConfig, AudioConfig, SpeechSynthesizer
#         speech_config = SpeechConfig(subscription_key=os.getenv("AZURE_SPEECH_KEY"), region=os.getenv("AZURE_SPEECH_REGION"))
#         synthesizer = SpeechSynthesizer(speech_config=speech_config, audio_config=AudioConfig())
#         result = synthesizer.speak_text(text)
#         return result.audio_data

__all__ = ["generate_spoken_brief"]
