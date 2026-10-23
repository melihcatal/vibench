import os
from typing import Dict
import google.cloud.translate_v2 as translate

# Using Google Cloud Translation for demonstration
# Environment variable expected: GOOGLE_APPLICATION_CREDENTIALS

def translate_welcome(locale: str, welcome_text: str) -> str:
    """Translate onboarding copy into the user's locale using Google Cloud Translation.","""    client = translate.Client()
    # Detect target locale if needed, here we assume locale is ISO 639-1 code
    result = client.translate(welcome_text, target_language=locale)
    return result['translatedText']


# Example of calling with sample data (helper function for later steps)
def sample_translate() -> Dict[str, str]:
    raw = "Welcome to our platform! Complete your profile and start exploring." 
    translations = {}
    translations['en'] = raw  # English source
    translations['es'] = translate_welcome('es', raw)
    translations['fr'] = translate_welcome('fr', raw)
    translations['de'] = translate_welcome('de', raw)
    return translations
