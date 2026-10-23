import os
from openai import OpenAI
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.translation.text import TextTranslationClient, TranslatorCredential
from azure.cognitiveservices.speech import SpeechConfig, SpeechSynthesizer


class ModelClient:
    _openai_client = None
    _content_safety_client = None
    _translation_client = None
    _speech_synthesizer = None

    @classmethod
    def get_openai_client(cls):
        if cls._openai_client is None:
            api_key = os.environ.get("OPENAI_API_KEY")
            if not api_key:
                raise ValueError("OPENAI_API_KEY environment variable not set.")
            cls._openai_client = OpenAI(api_key=api_key)
        return cls._openai_client

    @classmethod
    def get_content_safety_client(cls):
        if cls._content_safety_client is None:
            endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
            key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")
            if not endpoint or not key:
                raise ValueError(
                    "AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables must be set."
                )
            cls._content_safety_client = ContentSafetyClient(
                endpoint, AzureKeyCredential(key)
            )
        return cls._content_safety_client

    @classmethod
    def get_translation_client(cls):
        if cls._translation_client is None:
            endpoint = os.environ.get("AZURE_TRANSLATOR_ENDPOINT")
            key = os.environ.get("AZURE_TRANSLATOR_KEY")
            region = os.environ.get("AZURE_TRANSLATOR_REGION")
            if not endpoint or not key or not region:
                raise ValueError(
                    "AZURE_TRANSLATOR_ENDPOINT, AZURE_TRANSLATOR_KEY, and AZURE_TRANSLATOR_REGION environment variables must be set."
                )
            cls._translation_client = TextTranslationClient(
                endpoint=endpoint, credential=TranslatorCredential(key, region)
            )
        return cls._translation_client

    @classmethod
    def get_speech_synthesizer(cls):
        if cls._speech_synthesizer is None:
            speech_key = os.environ.get("AZURE_SPEECH_KEY")
            speech_region = os.environ.get("AZURE_SPEECH_REGION")
            if not speech_key or not speech_region:
                raise ValueError(
                    "AZURE_SPEECH_KEY and AZURE_SPEECH_REGION environment variables must be set."
                )
            speech_config = SpeechConfig(subscription=speech_key, region=speech_region)
            cls._speech_synthesizer = SpeechSynthesizer(speech_config=speech_config)
        return cls._speech_synthesizer
