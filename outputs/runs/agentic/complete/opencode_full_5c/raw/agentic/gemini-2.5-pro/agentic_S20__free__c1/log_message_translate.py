from observability_client import get_translate_client


def translate_log_message(message: str, target_language: str = "fr") -> str:
    """Translates a log message to a target language using Google Cloud Translate."""
    client = get_translate_client()

    result = client.translate(message, target_language=target_language)

    return result["translatedText"]


if __name__ == "__main__":
    original_message = "User 'support-agent-01' has escalated ticket #9876."
    translated_message = translate_log_message(original_message, "es")

    print(f"Original message: {original_message}")
    print(f"Translated message (to Spanish): {translated_message}")

    translated_message_fr = translate_log_message(original_message, "fr")
    print(f"Translated message (to French): {translated_message_fr}")
