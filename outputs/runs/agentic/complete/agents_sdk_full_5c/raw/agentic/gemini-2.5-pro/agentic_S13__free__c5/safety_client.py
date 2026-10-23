import os
from typing import Optional

from googleapiclient.discovery import build as build_google_api_client
from openai import OpenAI
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
import cohere
import deepl
import anthropic
from elevenlabs.client import ElevenLabs

def get_openai_client() -> OpenAI:
    """Initializes the OpenAI client using API key from environment variables."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")
    return OpenAI(api_key=api_key)

def get_azure_content_safety_client() -> ContentSafetyClient:
    """Initializes the Azure Content Safety client."""
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    api_key = os.getenv("AZURE_CONTENT_SAFETY_KEY")
    if not endpoint or not api_key:
        raise ValueError("Azure Content Safety credentials are not set in environment variables.")
    return ContentSafetyClient(endpoint, AzureKeyCredential(api_key))

def get_google_perspective_client():
    """Initializes the Google Perspective API client."""
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")
    # Note: The 'build' function can cause linting errors in some environments
    # due to its dynamic nature, but it is the standard way to use this library.
    return build_google_api_client(
        "commentanalyzer", "v1alpha1", developerKey=api_key, static_discovery=False
    )

def get_hive_api_key() -> str:
    """Gets the Hive Moderation API key."""
    api_key = os.getenv("HIVE_API_KEY")
    if not api_key:
        raise ValueError("HIVE_API_KEY environment variable not set.")
    return api_key
    
def get_cohere_client() -> cohere.Client:
    """Initializes the Cohere client."""
    api_key = os.getenv("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY environment variable not set.")
    return cohere.Client(api_key)

def get_deepl_translator() -> deepl.Translator:
    """Initializes the DeepL translator client."""
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable not set.")
    return deepl.Translator(auth_key)

def get_anthropic_client() -> anthropic.Anthropic:
    """Initializes the Anthropic client."""
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable not set.")
    return anthropic.Anthropic(api_key=api_key)

def get_elevenlabs_client() -> ElevenLabs:
    """Initializes the ElevenLabs client."""
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        raise ValueError("ELEVENLABS_API_KEY environment variable not set.")
    return ElevenLabs(api_key=api_key)
