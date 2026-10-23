from typing import List, Dict, Any, Optional
from google.cloud import translate_v3 as translate

def translate_document_fields(document: Dict[str, Any], fields_to_translate: List[str], target_language_code: str, project_id: str, location: str = "global") -> Optional[Dict[str, Any]]:
    """Translates specified user-facing fields within a document using Google Cloud Translation API.

    Args:
        document (Dict[str, Any]): The document containing fields to translate.
        fields_to_translate (List[str]): A list of field names whose values should be translated.
        target_language_code (str): The BCP-47 language code to translate into (e.g., "es" for Spanish).
        project_id (str): Your Google Cloud project ID.
        location (str): The location of the Translation API endpoint (e.g., "global" or a specific region).

    Returns:
        Optional[Dict[str, Any]]: A new document dictionary with translated fields, or None if translation fails.
    """
    client = translate.TranslationServiceClient()
    # The `parent` parameter for the Translation API is typically in the format:
    # `projects/{project_id}/locations/{location}`
    parent = f"projects/{project_id}/locations/{location}"

    translated_document = document.copy()
    texts_to_translate = []
    field_map = {}

    for field in fields_to_translate:
        if field in document and isinstance(document[field], str):
            texts_to_translate.append(document[field])
            field_map[len(texts_to_translate) - 1] = field # Map index back to original field name

    if not texts_to_translate:
        print("No translatable string fields found in the document for the given fields_to_translate.")
        return translated_document

    try:
        response = client.translate_text(
            request={
                "parent": parent,
                "contents": texts_to_translate,
                "target_language_code": target_language_code,
                "mime_type": "text/plain",  # Mime type of the input text. Currently only 'text/plain' is supported.
            }
        )

        for i, translation in enumerate(response.translations):
            original_field = field_map.get(i)
            if original_field:
                translated_document[original_field] = translation.translated_text
        
        print(f"Successfully translated fields for document to {target_language_code}.")
        return translated_document

    except Exception as e:
        print(f"Error translating document fields: {e}")
        return None

if __name__ == "__main__":
    # Example Usage:
    # Replace 'your-gcp-project-id' with your actual Google Cloud Project ID
    # Ensure you have enabled the Cloud Translation API and have appropriate permissions.
    # For local execution, ensure gcloud is authenticated or GOOGLE_APPLICATION_CREDENTIALS is set.
    GCP_PROJECT_ID = "your-gcp-project-id" # <<< IMPORTANT: Update this to your GCP Project ID

    sample_document = {
        "id": "product_xyz",
        "name": "Smart Coffee Maker",
        "description": "A coffee maker that can be controlled via a smartphone app. Features include custom brew settings and scheduled brewing.",
        "features": ["app_control", "custom_brew"], # This will not be translated as it's not a string
        "category": "Kitchen Appliances",
        "price": 129.99
    }
    fields_to_translate = ["name", "description"]
    target_lang = "es" # Spanish

    print(f"\nOriginal Document: {sample_document}")
    print(f"Attempting to translate fields {fields_to_translate} to {target_lang}...")
    try:
        translated_doc = translate_document_fields(
            sample_document, fields_to_translate, target_lang, GCP_PROJECT_ID
        )

        if translated_doc:
            print("\n--- Translated Document ---")
            print(translated_doc)
            print("---------------------------")
        else:
            print("Failed to translate document fields.")

        # Example with a field that doesn't exist
        print("\nAttempting to translate with a non-existent field...")
        translated_doc_no_exist = translate_document_fields(
            sample_document, ["name", "non_existent_field"], "fr", GCP_PROJECT_ID
        )
        if translated_doc_no_exist:
            print("Document with non-existent field translated (only existing fields affected):", translated_doc_no_exist)

    except Exception as e:
        print(f"Example usage failed: {e}")
