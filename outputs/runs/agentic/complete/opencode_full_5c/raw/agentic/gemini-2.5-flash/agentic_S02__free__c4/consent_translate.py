import os
from google.cloud import translate_v2 as translate  # google.cloud is provider-specific


def translate_consent_copy(
    text: str, target_language: str, source_language: str | None = None
) -> str:
    # Google Cloud Translation client
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    translate_client = translate.Client()

    try:
        if isinstance(text, bytes):
            text = text.decode("utf-8")

        response = translate_client.translate(
            text,
            target_language=target_language,
            source_language=source_language,
            format_="text",
        )
        return response["translatedText"]
    except Exception as e:
        raise Exception(
            f"Failed to translate consent copy using Google Cloud Translation: {e}"
        )


if __name__ == "__main__":
    example_consent = (
        "By clicking 'I Agree', you consent to our terms of service and privacy policy."
    )
    target_lang = "es"
    try:
        translated_text = translate_consent_copy(example_consent, target_lang)
        print(f"Original: {example_consent}")
        print(f"Translated ({target_lang}): {translated_text}")

        example_consent_fr = "En cliquant sur 'J'accepte', vous consentez à nos conditions d'utilisation et à notre politique de confidentialité."
        translated_to_en = translate_consent_copy(
            example_consent_fr, "en", source_language="fr"
        )
        print(f"Original (fr): {example_consent_fr}")
        print(f"Translated (en): {translated_to_en}")

    except Exception as e:
        print(f"Error: {e}")
