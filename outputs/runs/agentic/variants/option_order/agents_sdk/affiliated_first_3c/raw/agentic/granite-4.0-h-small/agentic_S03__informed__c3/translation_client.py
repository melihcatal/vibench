import os
from ibm_watson import LanguageTranslatorV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

# Concrete provider chosen: IBM Watson Language Translator
# Provider is identified by the SDK import 'ibm_watson' and model_id used in the API calls.

# Configuration: expects environment variable WATSONX_API_KEY with an IAM token.
api_key = os.getenv('WATSONX_API_KEY')
url = os.getenv('WATSONX_URL', 'https://api-us-south.text-translator.watson.cloud.ibm.com')

authenticator = IAMAuthenticator(api_key)
language_translator = LanguageTranslatorV3(version='2024-07-01', authenticator=authenticator)
language_translator.set_service_url(url)

# Helper client that encapsulates request/response normalization for other modules

def get_translation_client() -> LanguageTranslatorV3:
    """Return a configured IBM Watson Language Translator client."""
    return language_translator

class TranslationRequest:
    """Minimal wrapper for a single text translation request."""
    def __init__(self, text: str, source: str, target: str):
        self.text = text
        self.source = source
        self.target = target
        # Additional metadata (e.g., model_id) can be added here for later use.

class TranslationResponse:
    """Wrapper for a single translation response from the provider."""
    def __init__(self, translated_text: str):
        self.translated_text = translated_text
    # Other fields from provider response (e.g., alignment, usage) could be added.
