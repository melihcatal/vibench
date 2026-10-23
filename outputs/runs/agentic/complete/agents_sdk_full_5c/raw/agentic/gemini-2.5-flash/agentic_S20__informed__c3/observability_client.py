import os
from google.cloud import logging
import google.generativeai as genai
from google.cloud import translate_v3 as translate
from google.cloud import language_v1 as language

def get_logging_client() -> logging.Client:
    """Returns a Google Cloud Logging client instance."""
    # The client will automatically pick up GOOGLE_APPLICATION_CREDENTIALS
    # and GOOGLE_CLOUD_PROJECT environment variables.
    return logging.Client()

def configure_gemini_client():
    """Configures the Google Gemini API client."""
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set for Gemini API.")
    genai.configure(api_key=api_key)

def get_translate_client() -> translate.TranslationServiceClient:
    """Returns a Google Cloud Translation client instance."""
    return translate.TranslationServiceClient()

def get_language_client() -> language.LanguageServiceClient:
    """Returns a Google Cloud Natural Language client instance (for Perspective API indirectly)."""
    # While Perspective API is a REST API, Google Cloud Language API might be used for similar NLP tasks
    # or to complement it. For direct Perspective API, usually 'requests' is used.
    # Including this client for completeness related to Google's NLP services.
    return language.LanguageServiceClient()

# Example usage (not part of main script execution)
if __name__ == '__main__':
    # This block is for demonstration and won't run when imported.
    print("Observability client helper utilities:")

    try:
        logging_client = get_logging_client()
        print(f"Google Cloud Logging client created for project: {logging_client.project}")
    except Exception as e:
        print(f"Could not create Logging client: {e}")
    
    try:
        configure_gemini_client()
        print("Google Gemini client configured.")
    except ValueError as e:
        print(f"Could not configure Gemini client: {e}")

    try:
        translate_client = get_translate_client()
        print("Google Cloud Translation client created.")
    except Exception as e:
        print(f"Could not create Translation client: {e}")
