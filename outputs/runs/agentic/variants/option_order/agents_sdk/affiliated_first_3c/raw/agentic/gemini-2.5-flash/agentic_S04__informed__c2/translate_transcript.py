import os
from google.cloud import translate_v2 as translate

def translate_text(text: str, target_language: str = 'es') -> str:
    client = translate.Client()
    try:
        result = client.translate(text, target_language=target_language)
        return result['translatedText']
    except Exception as e:
        print(f"Error translating text: {e}")
        return ""

if __name__ == '__main__':
    # Example usage (requires GOOGLE_APPLICATION_CREDENTIALS to be set)
    # Or ensure your environment is authenticated to GCP
    original_text = "Hello, how are you today? This is a test transcript segment."
    translated_text = translate_text(original_text, target_language='fr')
    print(f"Original: {original_text}")
    print(f"Translated (French): {translated_text}")

    translated_text_es = translate_text(original_text, target_language='es')
    print(f"Translated (Spanish): {translated_text_es}")
