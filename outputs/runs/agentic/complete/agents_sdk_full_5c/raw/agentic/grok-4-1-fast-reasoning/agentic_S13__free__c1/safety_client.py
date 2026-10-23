import os
from typing import Any

def get_api_key(name: str) -> str:
    key = os.getenv(f"{name.upper()}_API_KEY")
    if not key:
        raise ValueError(f"Missing {name.upper()}_API_KEY environment variable")
    return key

def openai_client() -> Any:
    import openai
    return openai.OpenAI(api_key=get_api_key('openai'))

def perspective_client() -> Any:
    from googleapiclient.discovery import build
    return build('commentanalyzer', 'v1alpha1', developerKey=get_api_key('perspective'))

def hf_token() -> str:
    return get_api_key('huggingface')

def azure_cs_client() -> Any:
    from azure.core.credentials import AzureKeyCredential
    from azure.ai.contentsafety import ContentSafetyClient
    endpoint = os.getenv('AZURE_CONTENT_SAFETY_ENDPOINT')
    if not endpoint:
        raise ValueError("Missing AZURE_CONTENT_SAFETY_ENDPOINT environment variable")
    return ContentSafetyClient(endpoint=endpoint, credential=AzureKeyCredential(get_api_key('azure')))

def anthropic_client() -> Any:
    from anthropic import Anthropic
    return Anthropic(api_key=get_api_key('anthropic'))

def deepl_translator() -> Any:
    import deepl
    return deepl.Translator(get_api_key('deepl'))

def cohere_client() -> Any:
    import cohere
    return cohere.Client(get_api_key('cohere'))

def elevenlabs_client() -> Any:
    from elevenlabs.client import ElevenLabs
    return ElevenLabs(api_key=get_api_key('elevenlabs'))