from observability_client import GoogleTranslateClient
from observability_models import TranslatedMessage
from typing import List

def translate_log_messages(log_messages: List[str], target_language: str) -> List[TranslatedMessage]:
    google_translate_client = GoogleTranslateClient()
    translated_results: List[TranslatedMessage] = []

    for message in log_messages:
        translated_text = google_translate_client.translate_text(message, target_language)
        translated_results.append(TranslatedMessage(
            original_text=message,
            translated_text=translated_text,
            target_language=target_language
        ))
    return translated_results

if __name__ == "__main__":
    # Example log messages
    sample_log_messages = [
        "User login failed for invalid credentials.",
        "Database connection error: Timeout expired.",
        "New order placed by customer_id: 1001."
    ]

    target_lang_es = "es"
    target_lang_fr = "fr"

    print(f"Translating log messages to {target_lang_es.upper()}...")
    translated_es = translate_log_messages(sample_log_messages, target_lang_es)
    for res in translated_es:
        print(f"Original: {res.original_text}")
        print(f"Translated ({res.target_language}): {res.translated_text}")
    
    print(f"\nTranslating log messages to {target_lang_fr.upper()}...")
    translated_fr = translate_log_messages(sample_log_messages, target_lang_fr)
    for res in translated_fr:
        print(f"Original: {res.original_text}")
        print(f"Translated ({res.target_language}): {res.translated_text}")
