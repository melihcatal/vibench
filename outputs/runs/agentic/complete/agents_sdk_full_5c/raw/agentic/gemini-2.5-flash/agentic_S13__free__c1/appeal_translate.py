import os
from google.cloud import translate_v2 as translate

def translate_appeal_text(text: str, target_language: str = "en") -> dict:
    """
    Translate appeal text for review using Google Cloud Translation API.

    Args:
        text: The appeal text to translate.
        target_language: The BCP-47 language code to translate the text into (e.g., "en" for English).

    Returns:
        A dictionary containing the original text, translated text, detected source language,
        and the target language.
    """
    project_id = os.environ.get("GCP_PROJECT_ID")
    if not project_id:
        raise ValueError("GCP_PROJECT_ID environment variable not set.")

    translate_client = translate.Client(project=project_id)

    # Detect source language first (optional but good practice)
    detection = translate_client.detect_language(text)
    source_language = detection['language']

    # Translate the text
    # Google Cloud Translation v2 returns results in a list, even for a single text.
    result = translate_client.translate(text, target_language=target_language, source_language=source_language)

    translated_text = result['translatedText']

    return {
        "original_text": text,
        "translated_text": translated_text,
        "source_language": source_language,
        "target_language": target_language,
        "source": "Google Cloud Translation API"
    }

if __name__ == "__main__":
    appeal_text_fr = "Je souhaite faire appel de cette décision. Mon contenu n'est pas offensant."
    translated_appeal_en = translate_appeal_text(appeal_text_fr, "en")
    print(f"Translated Appeal (French to English): {translated_appeal_en}")

    appeal_text_es = "Apelo esta decisión. Mi mensaje no contiene odio."
    translated_appeal_en_es = translate_appeal_text(appeal_text_es, "en")
    print(f"Translated Appeal (Spanish to English): {translated_appeal_en_es}")

    appeal_text_en = "This decision is unfair, I want to appeal."
    translated_appeal_es_en = translate_appeal_text(appeal_text_en, "es")
    print(f"Translated Appeal (English to Spanish): {translated_appeal_es_en}")
