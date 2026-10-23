import os
from google.cloud import translate_v2 as translate
from typing import List, Dict, Any

# Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set.
# For example: export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/keyfile.json"

def translate_consent_copy(texts: List[str], target_language: str, source_language: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Translates identity-provider consent copy using Google Cloud Translation.
    
    Args:
        texts: A list of strings representing the consent copy to translate.
        target_language: The language to translate the text into (e.g., "es", "fr").
        source_language: The language of the input text (e.g., "en"). If not provided,
                         the service will attempt to detect the source language.
                         
    Returns:
        A list of dictionaries, each containing the translated text and source language.
        Example: [{"translatedText": "Hola Mundo", "detectedSourceLanguage": "en"}]
    """
    translate_client = translate.Client()

    translations = []
    for text in texts:
        if source_language:
            result = translate_client.translate(text, target_language=target_language, source_language=source_language)
        else:
            result = translate_client.translate(text, target_language=target_language)
        translations.append(result)
        
    return translations

if __name__ == "__main__":
    consent_texts = [
        "By logging in, you agree to our Terms of Service and Privacy Policy.",
        "We need your consent to access your basic profile information.",
        "Do you wish to proceed?"
    ]
    target_lang = "es"
    
    print(f"Translating consent copy to {target_lang}:")
    translated_results = translate_consent_copy(consent_texts, target_language=target_lang, source_language="en")
    
    for i, result in enumerate(translated_results):
        print(f"Original {i+1}: '{consent_texts[i]}'")
        print(f"Translated {i+1}: '{result['translatedText']}' (Source: {result.get('detectedSourceLanguage', 'N/A')})\n")

    print("Translating to French (auto-detect source language):")
    translated_results_fr = translate_consent_copy(["J'accepte les conditions.", "I agree to the terms."], target_language="fr")
    for i, result in enumerate(translated_results_fr):
        print(f"Translated {i+1}: '{result['translatedText']}' (Source: {result.get('detectedSourceLanguage', 'N/A')})\n")
