import os
from google.cloud import translate_v2 as translate


def translate_query(
    query: str, target_language: str, source_language: str = "en"
) -> str:
    """
    Translates a query to the target language for multilingual search.
    """
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv(
        "GOOGLE_APPLICATION_CREDENTIALS", "gcp_credentials.json"
    )
    translate_client = translate.Client()

    if isinstance(query, bytes):
        query = query.decode("utf-8")

    result = translate_client.translate(
        query, target_language=target_language, source_language=source_language
    )

    return result["translatedText"]


if __name__ == "__main__":
    english_query = "What are the best tourist attractions in Paris?"

    # Translate to Spanish
    spanish_translation = translate_query(english_query, "es")
    print(f"Original (en): {english_query}")
    print(f"Translated (es): {spanish_translation}")

    # Translate to French
    french_translation = translate_query(english_query, "fr")
    print(f"Translated (fr): {french_translation}")
