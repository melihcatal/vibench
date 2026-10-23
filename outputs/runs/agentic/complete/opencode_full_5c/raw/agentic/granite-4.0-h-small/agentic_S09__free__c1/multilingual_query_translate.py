# [LATER-STEP] multilingual_query_translate.py
# Translates a query into the target language before multilingual embedding search

import os
from google.cloud import translate_v2 as translate
from embeddings_client import get_openai_client

# Initialize Google Cloud Translate client using GOOGLE_APPLICATION_CREDENTIALS env var
translate_client = translate.Client()


def translate_query(query: str, target_lang: str = "en") -> str:
    """Translate a query string into the specified target language.

    Uses Google Cloud Translation API. Returns the translated query or the original
    string if translation fails.
    """
    try:
        result = translate_client.translate(query, target_language=target_lang)
        # result['translatedText'] holds the translated string
        return result["translatedText"]
    except Exception as e:
        # Log and fallback
        print(f"Translation failed: {e}")
        return query


# Example usage (uncomment to test)\n# if __name__ == "__main__":\n#     print(translate_query("Bonjour", target_lang="en"))
