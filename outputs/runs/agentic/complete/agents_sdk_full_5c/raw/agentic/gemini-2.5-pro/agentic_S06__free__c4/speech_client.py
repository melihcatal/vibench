"""
Provides configuration and client helper utilities for Text-to-Speech and related services.

This module centralizes the initialization of various third-party clients.
It relies on environment variables for API keys and configuration.
"""

import os
import boto3
import cohere
import deepl
import elevenlabs
import openai
import assemblyai
from google.cloud import texttospeech
from azure.cognitiveservices.speech import SpeechConfig

def get_google_tts_client():
    """Returns an authenticated Google Cloud Text-to-Speech client."""
    # Assumes GOOGLE_APPLICATION_CREDENTIALS is set in the environment
    return texttospeech.TextToSpeechClient()

def get_polly_client():
    """Returns an authenticated AWS Polly client."""
    # Assumes AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, and AWS_REGION are set
    return boto3.client(
        "polly",
        region_name=os.getenv("AWS_REGION", "us-east-1")
    )

def get_azure_speech_config():
    """Returns an Azure Speech Service configuration object."""
    subscription_key = os.getenv("AZURE_TTS_KEY")
    region = os.getenv("AZURE_TTS_REGION", "eastus")
    if not subscription_key:
        raise ValueError("AZURE_TTS_KEY environment variable not set.")
    return SpeechConfig(subscription=subscription_key, region=region)

def get_elevenlabs_client():
    """Returns an authenticated ElevenLabs client."""
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        raise ValueError("ELEVENLABS_API_KEY environment variable not set.")
    return elevenlabs.ElevenLabs(api_key=api_key)

def get_deepl_translator():
    """Returns an authenticated DeepL translator client."""
    api_key = os.getenv("DEEPL_API_KEY")
    if not api_key:
        raise ValueError("DEEPL_API_KEY environment variable not set.")
    return deepl.Translator(api_key)

def get_openai_client():
    """Returns an authenticated OpenAI client."""
    # Assumes OPENAI_API_KEY is set in the environment
    return openai.OpenAI()

def get_cohere_client():
    """Returns an authenticated Cohere client."""
    api_key = os.getenv("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY environment variable not set.")
    return cohere.Client(api_key)

def get_assemblyai_transcriber():
    """Returns an authenticated AssemblyAI transcriber client."""
    api_key = os.getenv("ASSEMBLYAI_API_KEY")
    if not api_key:
        raise ValueError("ASSEMBLYAI_API_KEY environment variable not set.")
    assemblyai.settings.api_key = api_key
    return assemblyai.Transcriber()
