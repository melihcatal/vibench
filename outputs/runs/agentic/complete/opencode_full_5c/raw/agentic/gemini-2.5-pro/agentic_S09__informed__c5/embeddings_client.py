import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()


def get_embeddings_client():
    """
    Configures and returns a Google Generative AI client.
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY not found in environment variables.")

    genai.configure(api_key=api_key)
    return genai


def get_openai_client():
    """
    Returns an OpenAI client.
    """
    from openai import OpenAI

    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def get_azure_content_safety_client():
    """
    Returns an Azure AI Content Safety client.
    """
    from azure.ai.contentsafety import ContentSafetyClient
    from azure.core.credentials import AzureKeyCredential

    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")
    if not endpoint or not key:
        raise ValueError("Azure Content Safety credentials not found.")
    return ContentSafetyClient(endpoint, AzureKeyCredential(key))


def get_deepl_translator():
    """
    Returns a DeepL translator client.
    """
    import deepl

    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY not found.")
    return deepl.Translator(auth_key)


def get_elevenlabs_client():
    """
    Returns an ElevenLabs client.
    """
    from elevenlabs import set_api_key

    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        raise ValueError("ELEVENLABS_API_KEY not found.")
    set_api_key(api_key)
    from elevenlabs.client import ElevenLabs

    return ElevenLabs()
