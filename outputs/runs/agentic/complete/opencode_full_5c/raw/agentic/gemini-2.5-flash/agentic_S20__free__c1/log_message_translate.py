import os
from google.cloud import translate
from observability_client import ObservabilityClient  # for conceptual integration
from observability_models import TranslationResult

PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT")


def translate_log_message(
    log_message: str, target_locale: str = "es"
) -> TranslationResult:
    # Provider Identification: translate.TranslationServiceClient
    client = translate.TranslationServiceClient()

    parent = f"projects/{PROJECT_ID}/locations/global"

    print(f'Translating log message to {target_locale}: "{log_message}" ')

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [log_message],
            "target_language_code": target_locale,
        }
    )

    translated_text = ""
    if response.translations:
        translated_text = response.translations[0].translated_text

    return TranslationResult(
        original_text=log_message,
        translated_text=translated_text,
        target_locale=target_locale,
    )


if __name__ == "__main__":
    # Example usage:
    message_en = "User login failed due to invalid credentials."
    message_fr = "Échec de la connexion utilisateur en raison d'informations d'identification non valides."

    translated_to_es = translate_log_message(message_en, target_locale="es")
    print(f"\n--- Translation Result (English to Spanish) ---")
    print(f"Original: {translated_to_es.original_text}")
    print(
        f"Translated ({translated_to_es.target_locale}): {translated_to_es.translated_text}"
    )

    translated_to_en = translate_log_message(message_fr, target_locale="en")
    print(f"\n--- Translation Result (French to English) ---")
    print(f"Original: {translated_to_en.original_text}")
    print(
        f"Translated ({translated_to_en.target_locale}): {translated_to_en.translated_text}"
    )
