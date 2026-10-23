import os
from google.cloud import translate_v2 as translate
from dotenv import load_dotenv

load_dotenv()


def translate_query(query: str, target_language: str = "en") -> dict:
    """
    Translates queries before multilingual embedding search using Google Cloud Translation.
    """
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set or authenticated
    # For local development, you might set this to the path of your service account key file.
    # e.g., os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/your/keyfile.json"

    translate_client = translate.Client()

    result = translate_client.translate(query, target_language=target_language)

    return {
        "translated_text": result["""translatedText"""],
        "detected_source_language": result["""detectedSourceLanguage"""],
    }


if __name__ == "__main__":
    sample_query_es = "Hola, ¿cómo estás?"
    sample_query_fr = "Où est la bibliothèque?"

    translation_es = translate_query(sample_query_es, "en")
    print(f"Original (ES): '{sample_query_es}'")
    print(
        f"Translated (EN): '{translation_es['''translated_text''']}' (Detected: {translation_es['''detected_source_language''']})"
    )

    translation_fr = translate_query(sample_query_fr, "en")
    print(f"Original (FR): '{sample_query_fr}'")
    print(
        f"Translated (EN): '{translation_fr['''translated_text''']}' (Detected: {translation_fr['''detected_source_language''']})"
    )
