import os
from google.cloud import translate_v3 as translate
from typing import List, Dict, Any

def translate_log_messages(messages: List[str], target_language_code: str, project_id: str, location: str = "global") -> List[Dict[str, str]]:
    """Translates support-visible log messages for another locale using Google Cloud Translation API."""
    client = translate.TranslationServiceClient()
    parent = f"projects/{project_id}/locations/{location}"

    print(f"Translating {len(messages)} messages to {target_language_code}...")

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": messages,
            "target_language_code": target_language_code,
        }
    )

    translated_results = []
    for i, translation in enumerate(response.translations):
        translated_results.append({
            "original_message": messages[i],
            "translated_message": translation.translated_text,
            "target_language_code": target_language_code
        })
    
    return translated_results

if __name__ == '__main__':
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        print("GOOGLE_CLOUD_PROJECT environment variable not set.")
        exit(1)

    log_messages_to_translate = [
        "User login failed due to invalid credentials.",
        "Database connection lost. Attempting to reconnect.",
        "新しい注文が処理されました。", # Japanese example
        "Se ha producido un error inesperado en el sistema.", # Spanish example
    ]
    target_lang = "es" # Translate to Spanish

    print("\n--- Log Message Translation (to Spanish) ---")
    translated_logs = translate_log_messages(log_messages_to_translate, target_lang, project_id)
    for res in translated_logs:
        print(f"Original: '{res['original_message']}'")
        print(f"Translated ({res['target_language_code']}): '{res['translated_message']}'\n")

    target_lang_jp = "ja" # Translate to Japanese
    print("\n--- Log Message Translation (to Japanese) ---")
    translated_logs_jp = translate_log_messages(log_messages_to_translate, target_lang_jp, project_id)
    for res in translated_logs_jp:
        print(f"Original: '{res['original_message']}'")
        print(f"Translated ({res['target_language_code']}): '{res['translated_message']}'\n")
