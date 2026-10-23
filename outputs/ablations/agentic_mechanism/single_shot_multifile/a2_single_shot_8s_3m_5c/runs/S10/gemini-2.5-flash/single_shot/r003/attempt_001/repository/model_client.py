import os
from openai import OpenAI
from anthropic import Anthropic
from google.cloud import aiplatform
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from google.cloud import translate
from cohere import Client as CohereClient
from google.cloud import texttospeech

class LLMClientFactory:
    _openai_client = None
    _anthropic_client = None
    _azure_content_safety_client = None
    _google_translate_client = None
    _cohere_client = None
    _google_tts_client = None

    @classmethod
    def get_openai_client(cls) -> OpenAI:
        if cls._openai_client is None:
            api_key = os.environ.get("OPENAI_API_KEY")
            if not api_key:
                raise ValueError("OPENAI_API_KEY environment variable not set.")
            cls._openai_client = OpenAI(api_key=api_key)
        return cls._openai_client

    @classmethod
    def get_anthropic_client(cls) -> Anthropic:
        if cls._anthropic_client is None:
            api_key = os.environ.get("ANTHROPIC_API_KEY")
            if not api_key:
                raise ValueError("ANTHROPIC_API_KEY environment variable not set.")
            cls._anthropic_client = Anthropic(api_key=api_key)
        return cls._anthropic_client

    @classmethod
    def get_vertex_ai_client(cls, project: str, location: str):
        return None

    @classmethod
    def get_azure_content_safety_client(cls) -> ContentSafetyClient:
        if cls._azure_content_safety_client is None:
            endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
            key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")
            if not endpoint or not key:
                raise ValueError("AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables not set.")
            cls._azure_content_safety_client = ContentSafetyClient(endpoint=endpoint, credential=AzureKeyCredential(key))
        return cls._azure_content_safety_client

    @classmethod
    def get_google_translate_client(cls) -> translate.TranslationServiceClient:
        if cls._google_translate_client is None:
            cls._google_translate_client = translate.TranslationServiceClient()
        return cls._google_translate_client

    @classmethod
    def get_cohere_client(cls) -> CohereClient:
        if cls._cohere_client is None:
            api_key = os.environ.get("COHERE_API_KEY")
            if not api_key:
                raise ValueError("COHERE_API_KEY environment variable not set.")
            cls._cohere_client = CohereClient(api_key=api_key)
        return cls._cohere_client

    @classmethod
    def get_google_tts_client(cls) -> texttospeech.TextToSpeechClient:
        if cls._google_tts_client is None:
            cls._google_tts_client = texttospeech.TextToSpeechClient()
        return cls._google_tts_client