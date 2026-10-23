import os
from openai import OpenAI
import boto3
from google.cloud import translate, language

class TranslationClients:
    """
    Provides initialized clients for various translation and related services.
    """
    _openai_client = None
    _google_translate_client = None
    _aws_translate_client = None
    _aws_polly_client = None
    _google_language_client = None
    _cohere_client = None

    @classmethod
    def get_openai_client(cls) -> OpenAI:
        if cls._openai_client is None:
            cls._openai_client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        return cls._openai_client

    @classmethod
    def get_google_translate_client(cls) -> translate.TranslationServiceClient:
        if cls._google_translate_client is None:
            cls._google_translate_client = translate.TranslationServiceClient()
        return cls._google_translate_client
    
    @classmethod
    def get_google_language_client(cls) -> language.LanguageServiceClient:
        if cls._google_language_client is None:
            cls._google_language_client = language.LanguageServiceClient()
        return cls._google_language_client

    @classmethod
    def get_aws_translate_client(cls):
        if cls._aws_translate_client is None:
            cls._aws_translate_client = boto3.client("translate", region_name=os.environ.get("AWS_REGION"))
        return cls._aws_translate_client
    
    @classmethod
    def get_aws_polly_client(cls):
        if cls._aws_polly_client is None:
            cls._aws_polly_client = boto3.client("polly", region_name=os.environ.get("AWS_REGION"))
        return cls._aws_polly_client
    
    @classmethod
    def get_cohere_client(cls):
        if cls._cohere_client is None:
            # Cohere client initialization would go here if using their SDK
            # For now, we'll assume direct HTTP calls or a simple wrapper
            pass
        return None # Placeholder, as DeepL and Cohere are assumed to be direct HTTP for simplicity in this exercise
