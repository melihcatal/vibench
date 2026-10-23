import os
from google.cloud import translate
from typing import Dict, Any, List

def translate_text_field(text: str, target_language: str, project_id: str) -> Dict[str, Any]:
    """
    Translates a single text field using Google Cloud Translation.
    Requires GOOGLE_APPLICATION_CREDENTIALS to be set.
    """
    client = translate.TranslationServiceClient()
    location = "global"
    parent = f"projects/{project_id}/locations/{location}"

    try:
        response = client.translate_text(
            request={
                "parent": parent,
                "contents": [text],
                "target_language_code": target_language,
            }
        )
        translations = []
        for translation in response.translations:
            translations.append(translation.translated_text)
        return {"status": "success", "original_text": text, "translations": translations, "target_language": target_language}
    except Exception as e:
        return {"status": "error", "message": f"Google Cloud Translation failed: {e}"}

def translate_document_fields(document: Dict[str, Any], fields_to_translate: List[str], target_language: str, project_id: str) -> Dict[str, Any]:
    """
    Translates specified fields within a document using Google Cloud Translation.
    """
    translated_document = document.copy()
    for field in fields_to_translate:
        if field in document and isinstance(document[field], str):
            translation_result = translate_text_field(document[field], target_language, project_id)
            if translation_result.get("status") == "success" and translation_result.get("translations"):
                translated_document[f"{field}_{target_language}"] = translation_result["translations"][0]
            else:
                print(f"Warning: Could not translate field '{field}': {translation_result.get("message", "Unknown error")}")
        else:
            print(f"Warning: Field '{field}' not found or not a string in document ID: {document.get("id", "N/A")}")
    return translated_document

if __name__ == '__main__':
    # Example usage (requires GOOGLE_APPLICATION_CREDENTIALS and GOOGLE_CLOUD_PROJECT_ID to be set up)
    # Set a dummy project_id for local testing if not using actual GCP project
    # In a real scenario, this would come from an environment variable or config
    PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT_ID", "your-gcp-project-id") 

    sample_document = {
        "id": "doc_002",
        "title": "Hello World",
        "description": "This is a sample document for translation."
    }
    fields = ["title", "description"]
    target_lang = "es"
    
    if PROJECT_ID == "your-gcp-project-id":
        print("Please set GOOGLE_CLOUD_PROJECT_ID environment variable for actual translation.")
        print("Using mock translation for demonstration.")
        translated_doc = sample_document.copy()
        translated_doc[f"title_{target_lang}"] = "Hola Mundo"
        translated_doc[f"description_{target_lang}"] = "Este es un documento de ejemplo para traducción."
    else:
        translated_doc = translate_document_fields(sample_document, fields, target_lang, PROJECT_ID)

    print(f"Translated Document: {translated_doc}")
