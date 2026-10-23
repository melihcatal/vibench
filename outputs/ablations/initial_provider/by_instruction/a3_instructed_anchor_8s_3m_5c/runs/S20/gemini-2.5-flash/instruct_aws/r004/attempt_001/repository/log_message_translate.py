import os
from typing import List, Dict
from google.cloud import translate_v2 as translate

def translate_log_messages(project_id: str, messages: List[str], target_language_code: str = 'es') -> List[Dict[str, str]]:
    client = translate.Client(project=project_id)

    translations = []
    for message in messages:
        result = client.translate(message, target_language=target_language_code)
        translations.append({
            "original": message,
            "translated": result['translatedText'],
            "detected_source_language": result['detectedSourceLanguage']
        })
    return translations

if __name__ == '__main__':
    PROJECT_ID = os.environ.get('GOOGLE_CLOUD_PROJECT')  # e.g., your-gcp-project-id

    if not PROJECT_ID:
        print("Please set the GOOGLE_CLOUD_PROJECT environment variable.")
    else:
        example_log_messages = [
            "User login successful for user_id: 123.",
            "Database connection error: Could not connect to host.",
            "Payment processed successfully. Transaction ID: TXN789."
        ]

        target_lang = "fr" # French
        print(f"Translating log messages to {target_lang.upper()}...")
        translated_results = translate_log_messages(PROJECT_ID, example_log_messages, target_language_code=target_lang)

        for res in translated_results:
            print(f"\nOriginal: {res['original']}")
            print(f"Translated ({target_lang}): {res['translated']}")
            print(f"Detected Source Language: {res['detected_source_language']}")
