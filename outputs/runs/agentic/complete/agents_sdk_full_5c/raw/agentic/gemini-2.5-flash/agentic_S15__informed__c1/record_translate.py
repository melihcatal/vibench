import os
from google.cloud import translate_v2 as translate

def translate_document_field(text: str, target_language: str = "es") -> str:
    """
    Translates a given text field using Google Cloud Translation.
    """
    # Requires GOOGLE_APPLICATION_CREDENTIALS to be set.
    # export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/key.json"

    translate_client = translate.Client()

    try:
        result = translate_client.translate(text, target_language=target_language)
        translated_text = result["translatedText"]
        print(f"Original text: '{text}', Translated to {target_language}: '{translated_text}'")
        return translated_text
    except Exception as e:
        print(f"Error translating text with Google Cloud Translation: {e}")
        return f"Error: Could not translate text. {e}"

if __name__ == "__main__":
    # Ensure GOOGLE_APPLICATION_CREDENTIALS is set for local testing
    
    text_to_translate = "Hello world, how are you today?"
    target_lang = "fr" # French

    try:
        translated_result = translate_document_field(text_to_translate, target_lang)
        print(f"Translation result for '{text_to_translate}' to {target_lang}: {translated_result}")

        another_text = "The quick brown fox jumps over the lazy dog."
        translated_german = translate_document_field(another_text, "de") # German
        print(f"Translation result for '{another_text}' to de: {translated_german}")
    except Exception as e:
        print(f"An error occurred during translation examples: {e}")
