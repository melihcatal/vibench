from google.cloud import translate
import os
from typing import List, Dict

def translate_queries_for_multilingual_search(queries: List[str], target_language: str = "en") -> Dict[str, str]:
    """Translates a list of queries to a target language using Google Cloud Translation.

    Args:
        queries: A list of query strings to translate.
        target_language: The BCP-47 language code of the target language (e.g., "en" for English).

    Returns:
        A dictionary mapping original queries to their translated versions.
    """
    # Google Cloud Translation client automatically uses GOOGLE_APPLICATION_CREDENTIALS
    # or other standard authentication methods if available in the environment.
    # No explicit API key is usually passed here for SDK; it relies on ADC.
    client = translate.TranslationServiceClient()
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT") # Or pass explicitly if needed

    if not project_id:
        print("Warning: GOOGLE_CLOUD_PROJECT environment variable not set. May impact some configurations.")
        # Attempt to get project ID from credentials if possible
        try:
            import google.auth
            credentials, project_id = google.auth.default()
            if not project_id:
                 raise ValueError("Could not determine Google Cloud Project ID. Set GOOGLE_CLOUD_PROJECT or ensure ADC is configured.")
        except Exception as e:
            raise ValueError(f"Failed to determine Google Cloud Project ID: {e}. Set GOOGLE_CLOUD_PROJECT or ensure ADC is configured.")

    location = "global"
    parent = f"projects/{project_id}/locations/{location}"

    translations = {}
    for query in queries:
        try:
            response = client.translate_text(
                request={
                    "parent": parent,
                    "contents": [query],
                    "target_language_code": target_language,
                }
            )
            # The response contains a list of translations for the contents provided.
            # We assume a single translation per query for simplicity here.
            if response.translations:
                translations[query] = response.translations[0].translated_text
            else:
                translations[query] = query # Return original if no translation found
        except Exception as e:
            translations[query] = f"ERROR: {str(e)}"
            print(f"Error translating \"{query}\": {e}")

    return translations

if __name__ == '__main__':
    sample_queries = [
        "¿Qué hora es?",
        "Comment allez-vous?",
        "こんにちは"
    ]
    target_lang = "en"

    print(f"Translating queries to {target_lang}...")
    try:
        translated_results = translate_queries_for_multilingual_search(sample_queries, target_lang)
        for original, translated in translated_results.items():
            print(f"Original: \"{original}\" -> Translated: \"{translated}\"")
    except ValueError as e:
        print(f"Configuration Error: {e}")
        print("Please ensure GOOGLE_CLOUD_PROJECT environment variable is set and Application Default Credentials are configured.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
