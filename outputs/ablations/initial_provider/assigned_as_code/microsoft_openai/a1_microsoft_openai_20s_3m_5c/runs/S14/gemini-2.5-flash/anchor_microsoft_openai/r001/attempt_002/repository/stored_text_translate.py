from google.cloud import translate_v2 as translate
import os

def stored_text_translate(payload):
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("Google Cloud Project ID not found in environment variables.")

    target_language = payload['target_language']
    text_content = payload['text_content']

    translate_client = translate.Client(project=project_id)

    # The Translation API can detect the source language automatically
    result = translate_client.translate(text_content, target_language=target_language)

    return {
        'translated_text': result['translatedText'],
        'original_text': result['input'],
        'source_language': result['detectedSourceLanguage'],
        'target_language': target_language
    }
