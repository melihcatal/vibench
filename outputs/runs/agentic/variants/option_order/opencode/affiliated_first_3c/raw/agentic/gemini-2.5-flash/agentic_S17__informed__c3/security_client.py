import os
from google.cloud import kms_v1
from google.cloud import translate_v3
import google.generativeai as genai
import requests


def get_kms_client():
    return kms_v1.KeyManagementServiceClient()


def get_gemini_model():
    # Make sure GOOGLE_API_KEY environment variable is set
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    return genai.GenerativeModel("gemini-pro")


def get_gemini_embedding_model():
    # Make sure GOOGLE_API_KEY environment variable is set
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    return "models/embedding-001"


def get_perspective_api_client():
    # Make sure PERSPECTIVE_API_KEY environment variable is set
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")
    return api_key, "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def get_translate_client():
    return translate_v3.TranslationServiceClient()
