from observability_client import get_translate_client


def translate_log_message(message: str, target_locale: str) -> str:
    translate_client = get_translate_client()

    result = translate_client.translate(message, target_language=target_locale)

    return result["translatedText"]


if __name__ == "__main__":
    log_message_en = "User 'support_agent' accessed customer records."
    target_language = "fr"

    translated_message = translate_log_message(log_message_en, target_language)

    print(f"Original message ({'en'}): {log_message_en}")
    print(f"Translated message ({target_language}): {translated_message}")
