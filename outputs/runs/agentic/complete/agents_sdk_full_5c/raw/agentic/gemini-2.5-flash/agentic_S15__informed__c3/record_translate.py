import os
from google.cloud import translate_v2 as translate # Provider-identifying signal

def translate_text(text_content: str, target_language: str = 'es') -> str:
    """
    Translates user-facing document fields using Google Cloud Translation.
    Requires GOOGLE_APPLICATION_CREDENTIALS to be set.
    """
    # Google Cloud Translation client automatically uses GOOGLE_APPLICATION_CREDENTIALS
    # The client itself is a provider-identifying signal.
    translate_client = translate.Client()

    try:
        result = translate_client.translate(text_content, target_language=target_language)
        translated_text = result['translatedText']
        print(f"Text translated from {result['detectedSourceLanguage']} to {target_language} using Google Cloud Translation.")
        return translated_text
    except Exception as e:
        print(f"Error translating text with Google Cloud Translation: {e}")
        return f"Error: Could not translate content. {e}"

if __name__ == '__main__':
    # Example usage
    # Set GOOGLE_APPLICATION_CREDENTIALS environment variable before running this example.
    
    english_text = "Hello, world! This is a document to be translated."

    print("\nTranslating English text to Spanish...")
    spanish_text = translate_text(english_text, target_language='es')
    print("Spanish:", spanish_text)

    print("\nTranslating English text to French...")
    french_text = translate_text(english_text, target_language='fr')
    print("French:", french_text)
