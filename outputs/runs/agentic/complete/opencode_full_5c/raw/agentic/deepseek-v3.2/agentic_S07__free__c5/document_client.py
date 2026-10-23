import os
from google.cloud import vision
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
from openai import OpenAI
from google.cloud import translate_v2 as translate


def get_vision_client():
    """Initialize and return Google Cloud Vision client."""
    credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    if not credentials_path:
        raise ValueError(
            "GOOGLE_APPLICATION_CREDENTIALS environment variable must be set"
        )

    return vision.ImageAnnotatorClient()


def get_form_recognizer_client():
    """Initialize and return Azure Form Recognizer client."""
    endpoint = os.getenv("AZURE_FORM_RECOGNIZER_ENDPOINT")
    key = os.getenv("AZURE_FORM_RECOGNIZER_KEY")

    if not endpoint or not key:
        raise ValueError(
            "AZURE_FORM_RECOGNIZER_ENDPOINT and AZURE_FORM_RECOGNIZER_KEY must be set"
        )

    return DocumentAnalysisClient(endpoint=endpoint, credential=AzureKeyCredential(key))


def get_openai_client():
    """Initialize and return OpenAI client."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable must be set")

    return OpenAI(api_key=api_key)


def get_translate_client():
    """Initialize and return Google Cloud Translate client."""
    credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    if not credentials_path:
        raise ValueError(
            "GOOGLE_APPLICATION_CREDENTIALS environment variable must be set"
        )

    return translate.Client()


def get_google_ai_client():
    """Initialize and return Google AI (Gemini) client."""
    import google.generativeai as genai

    api_key = os.getenv("GOOGLE_AI_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_AI_API_KEY environment variable must be set")

    genai.configure(api_key=api_key)
    return genai
