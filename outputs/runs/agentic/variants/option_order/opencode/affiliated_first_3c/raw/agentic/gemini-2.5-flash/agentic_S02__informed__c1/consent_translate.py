import os
from google.cloud import translate_v2 as translate


def translate_consent_copy(text: str, target_language: str) -> str:
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.environ.get(
        "GOOGLE_APPLICATION_CREDENTIALS_PATH"
    )  # Assuming path is set in env
    if not os.environ.get("GOOGLE_APPLICATION_CREDENTIALS_PATH"):
        raise ValueError(
            "Missing GOOGLE_APPLICATION_CREDENTIALS_PATH environment variable."
        )

    translate_client = translate.Client()

    try:
        result = translate_client.translate(text, target_language=target_language)
        return result["translatedText"]
    except Exception as e:
        print(f"Error translating text with Google Cloud Translation: {e}")
        return "Translation failed."


if __name__ == "__main__":
    english_consent = (
        "By logging in, you agree to our Terms of Service and Privacy Policy."
    )
    spanish_translation = translate_consent_copy(english_consent, "es")
    print("English:", english_consent)
    print("Spanish:", spanish_translation)

    french_translation = translate_consent_copy(english_consent, "fr")
    print("French:", french_translation)
