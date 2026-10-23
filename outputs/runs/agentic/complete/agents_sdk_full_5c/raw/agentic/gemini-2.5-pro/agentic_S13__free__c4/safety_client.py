"""Local client helpers and configuration for safety APIs."""
import os
from openai import OpenAI
from googleapiclient import discovery
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
import assemblyai as aai
import anthropic
import deepl
import cohere
from elevenlabs.client import ElevenLabs


def get_openai_client():
    """Returns an OpenAI client configured via environment variables."""
    return OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def get_perspective_client():
    """Returns a Google Perspective API client configured via environment variables."""
    api_key = os.environ.get("GOOGLE_API_KEY")
    return discovery.build(
        "commentanalyzer",
        "v1alpha1",
        developerKey=api_key,
        static_discovery=False,
    )

def get_azure_content_safety_client():
    """Returns an Azure Content Safety client configured via environment variables."""
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")
    if not endpoint or not key:
        raise ValueError("Azure Content Safety endpoint and key must be set.")
    return ContentSafetyClient(endpoint, AzureKeyCredential(key))

def get_assemblyai_client():
    """Configures and returns the AssemblyAI client."""
    aai.settings.api_key = os.environ.get("ASSEMBLYAI_API_KEY")
    return aai

def get_anthropic_client():
    """Returns an Anthropic client configured via environment variables."""
    return anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

def get_deepl_translator():
    """Returns a DeepL translator client."""
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    return deepl.Translator(auth_key)

def get_cohere_client():
    """Returns a Cohere client configured via environment variables."""
    return cohere.Client(os.environ.get("COHERE_API_KEY"))
    
def get_elevenlabs_client():
    """Returns an ElevenLabs client configured via environment variables."""
    return ElevenLabs(api_key=os.environ.get("ELEVENLABS_API_KEY"))
