from typing import List
from observability_client import ObservabilityClient
from observability_models import TranslatedMessage


def translate_log_messages(
    log_messages: List[str], target_language: str = "es"
) -> List[TranslatedMessage]:
    """Translates support-visible log messages for another locale using Google Cloud Translation API.

    Args:
        log_messages: A list of log message strings to translate.
        target_language: The target language code (e.g., "es" for Spanish, "fr" for French).

    Returns:
        A list of TranslatedMessage objects, one for each original log message.
    """
    client = ObservabilityClient().translate_client

    translations: List[TranslatedMessage] = []

    if not log_messages:
        return translations

    try:
        # The translate_client.translate method can take a list of texts
        response = client.translate(log_messages, target_language=target_language)

        for i, translation in enumerate(response):
            original_text = log_messages[i]
            translated_text = translation["translatedText"]
            translations.append(
                TranslatedMessage(original_text, translated_text, target_language)
            )
    except Exception as e:
        print(f"Error during translation: {e}")
        # In case of an error, return original messages with an error indicator
        for message in log_messages:
            translations.append(
                TranslatedMessage(message, f"Translation Error: {e}", target_language)
            )

    return translations


if __name__ == "__main__":
    # Example usage
    log_messages_to_translate = [
        "User login successful.",
        "Error: Database connection failed.",
        "Warning: Disk space is low.",
    ]

    print("\n--- Translating to Spanish (es) ---")
    spanish_translations = translate_log_messages(log_messages_to_translate, "es")
    for translated_msg in spanish_translations:
        print(f"Original: {translated_msg.original_text}")
        print(
            f"Translated ({translated_msg.target_language}): {translated_msg.translated_text}"
        )

    print("\n--- Translating to French (fr) ---")
    french_translations = translate_log_messages(log_messages_to_translate, "fr")
    for translated_msg in french_translations:
        print(f"Original: {translated_msg.original_text}")
        print(
            f"Translated ({translated_msg.target_language}): {translated_msg.translated_text}"
        )
