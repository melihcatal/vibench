import os
from typing import List
from google.cloud import translate_v3beta1 as translation_v3beta1

def translate_transcript_segments(text_segments: List[str], target_language: str, project_id: str) -> List[str]:
    """
    Translates a list of text segments using Google Cloud Translation API.

    Args:
        text_segments: A list of strings, where each string is a segment to be translated.
        target_language: The target language code (e.g., "es" for Spanish).
        project_id: Your Google Cloud project ID.

    Returns:
        A list of translated text segments.
    """
    if not project_id:
        raise ValueError("Google Cloud project ID must be provided.")

    client = translation_v3beta1.TranslationServiceClient()
    location = "global" # Or a specific region if required
    parent = f"projects/{project_id}/locations/{location}"

    translated_texts = []
    for text in text_segments:
        # The `translate_text` method can take a list of texts, but for simplicity
        # and to manage potential rate limits or larger requests, we'll iterate here.
        # For very large batch translations, consider using batch_translate_text.
        response = client.translate_text(
            request={
                "parent": parent,
                "contents": [text],
                "target_language_code": target_language,
            }
        )
        for translation in response.translations:
            translated_texts.append(translation.translated_text)
    
    return translated_texts

if __name__ == "__main__":
    # Example Usage:
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    # or authenticate your gcloud CLI.
    # export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/keyfile.json"
    # gcloud auth application-default login

    # project_id = os.environ.get("GOOGLE_CLOUD_PROJECT") # Or replace with your actual project ID
    # if not project_id:
    #     print("Please set the GOOGLE_CLOUD_PROJECT environment variable or replace with your project ID.")
    # else:
    #     segments_to_translate = [
    #         "Hello, how are you?",
    #         "This is a test sentence."
    #     ]
    #     target_lang = "es"
    #     print(f"Translating segments to {target_lang}...")
    #     try:
    #         translated_segments = translate_transcript_segments(segments_to_translate, target_lang, project_id)
    #         print("Translated Segments:")
    #         for original, translated in zip(segments_to_translate, translated_segments):
    #             print(f"  Original: {original}")
    #             print(f"  Translated: {translated}")
    #     except Exception as e:
    #         print(f"Error during translation: {e}")
    print("To run this example, set GOOGLE_APPLICATION_CREDENTIALS and GOOGLE_CLOUD_PROJECT environment variables and uncomment the test lines.")
