import os
from google.cloud import secretmanager

def get_secret_manager_client():
    """Returns a Google Secret Manager client."""
    return secretmanager.SecretManagerServiceClient()

def get_gemini_client():
    """Returns a Google Generative AI client."""
    # The google-genai library does not have an explicit client class
    # for API key authentication, it relies on `genai.configure` or environment variables.
    # We will simulate a "client" by returning the module itself.
    # In a real scenario, this would configure the API key if not already set.
    # For this exercise, we just indicate the module.
    import google.generativeai as genai
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    return genai

def get_translate_client():
    """Returns a Google Cloud Translation client."""
    from google.cloud import translate_v2 as translate
    return translate.Client()
