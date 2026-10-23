import os
import google.cloud.logging_v2
import google.generativeai as genai
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from google.cloud import translate_v3 as translate


def get_logging_client():
    # GOOGLE_APPLICATION_CREDENTIALS environment variable should be set
    if "GOOGLE_APPLICATION_CREDENTIALS" not in os.environ:
        raise ValueError("GOOGLE_APPLICATION_CREDENTIALS environment variable not set.")
    return google.cloud.logging_v2.Client()


def get_gemini_model(model_name: str = "gemini-pro"):
    if "GOOGLE_API_KEY" not in os.environ:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")
    genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
    return genai.GenerativeModel(model_name)


def get_content_safety_client():
    if (
        "AZURE_CONTENT_SAFETY_ENDPOINT" not in os.environ
        or "AZURE_CONTENT_SAFETY_KEY" not in os.environ
    ):
        raise ValueError(
            "AZURE_CONTENT_SAFETY_ENDPOINT or AZURE_CONTENT_SAFETY_KEY environment variables not set."
        )
    endpoint = os.environ["AZURE_CONTENT_SAFETY_ENDPOINT"]
    key = os.environ["AZURE_CONTENT_SAFETY_KEY"]
    return ContentSafetyClient(endpoint, AzureKeyCredential(key))


def get_translation_client():
    # GOOGLE_APPLICATION_CREDENTIALS environment variable should be set
    if "GOOGLE_APPLICATION_CREDENTIALS" not in os.environ:
        raise ValueError("GOOGLE_APPLICATION_CREDENTIALS environment variable not set.")
    return translate.TranslationServiceClient()
