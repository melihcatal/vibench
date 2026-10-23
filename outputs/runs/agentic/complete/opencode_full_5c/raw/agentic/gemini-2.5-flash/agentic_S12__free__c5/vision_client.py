import os
from google.cloud import vision_v1
import google.generativeai as genai
from google.cloud import translate_v3
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from google.cloud import storage


def get_vision_client():
    return vision_v1.ImageAnnotatorClient()


def get_gemini_pro_vision_model():
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    return genai.GenerativeModel("gemini-pro-vision")


def get_gemini_pro_model():
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    return genai.GenerativeModel("gemini-pro")


def get_translation_client():
    return translate_v3.TranslationServiceClient()


def get_azure_content_safety_client():
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")
    if not endpoint or not key:
        raise ValueError(
            "AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables must be set."
        )
    return ContentSafetyClient(endpoint, AzureKeyCredential(key))


def get_gcs_client():
    return storage.Client()
