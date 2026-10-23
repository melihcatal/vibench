import os
from google.cloud import translate_v2 as translate

def record_translate(document_records: list[dict], target_language: str = 'es') -> dict:
    """Translates user-facing document fields using Google Cloud Translation."""
    # Assumes GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    # or application default credentials are configured.
    translate_client = translate.Client()

    translation_results = []
    for record in document_records:
        text_to_translate = record.get("data", {}).get("text", "")
        if not text_to_translate:
            translation_results.append({"document_id": record.get("document_id"), "status": "skipped", "message": "No text content to translate."})
            continue

        try:
            result = translate_client.translate(
                text_to_translate, target_language=target_language)

            translation_results.append({
                "document_id": record.get("document_id"),
                "status": "success",
                "original_text": text_to_translate,
                "translated_text": result['translatedText'],
                "detected_source_language": result['detectedSourceLanguage']
            })
        except Exception as e:
            translation_results.append({"document_id": record.get("document_id"), "status": "error", "message": str(e)})

    return {"status": "success", "translations": translation_results}

if __name__ == '__main__':
    # This is a placeholder for local execution, not part of the core integration logic.
    # Ensure GOOGLE_APPLICATION_CREDENTIALS is set in your environment.
    pass
