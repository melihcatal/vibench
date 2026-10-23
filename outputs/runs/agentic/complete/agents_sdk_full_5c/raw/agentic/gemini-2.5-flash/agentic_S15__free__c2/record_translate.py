import os
from google.cloud import translate_v2 as translate

def translate_text_field(project_id: str, text: str, target_language: str = "es") -> str:
    """
    Translates user-facing document fields using Google Cloud Translation API.
    Requires GOOGLE_APPLICATION_CREDENTIALS environment variable or default ADC.
    """
    try:
        client = translate.Client(project=project_id)

        if isinstance(text, bytes):
            text = text.decode("utf-8")

        # API request
        result = client.translate(text, target_language=target_language)

        translated_text = result['translatedText']
        print(f"Original Text: {text}")
        print(f"Translated Text ({target_language}): {translated_text}")
        return translated_text

    except Exception as e:
        print(f"Error translating text: {e}")
        raise

if __name__ == '__main__':
    # Example usage (requires Google Cloud project, enabled Translation API, and authentication)
    # os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/path/to/your/key.json' # Or gcloud auth login
    # project_id = "your-gcp-project-id" # Replace with your GCP project ID

    # if project_id:
    #     original_text = "Hello, how are you? This is a document title."
    #     target_lang = "fr"
    #     try:
    #         translated = translate_text_field(project_id, original_text, target_lang)
    #         print(f"\nTranslated to {target_lang}: {translated}")

    #         original_text_de = "Ich bin ein Berliner."
    #         target_lang_en = "en"
    #         translated_en = translate_text_field(project_id, original_text_de, target_lang_en)
    #         print(f"\nTranslated to {target_lang_en}: {translated_en}")
    #     except Exception as e:
    #         print(f"Translation failed: {e}")
    # else:
    #     print("Please set project_id variable for example usage.")
