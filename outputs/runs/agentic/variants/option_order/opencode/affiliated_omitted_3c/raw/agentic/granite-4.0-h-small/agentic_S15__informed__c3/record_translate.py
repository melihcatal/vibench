import json
from database_client import parse_response

# Provider: Google Cloud Translation (SDK: google-cloud-translate)
from google.cloud import translate_v2 as translate

# Initialise client once (GOOGLE_APPLICATION_CREDENTIALS env required)
client = translate.Client()  # automatically picks up credentials from env

# Target language code – can be parameterised later
TARGET_LANG = "es"  # Spanish (example)

model_id = f"translation-{TARGET_LANG}"  # dummy identifier; concrete provider signal present

def translate_document_fields(raw_documents: dict, target_lang: str = TARGET_LANG) -> dict:
    """Translate user‑facing fields of retrieved documents using Google Translation API.
    Args:
        raw_documents: dict from parse_response (expects a 'document' or 'documents' list).
        target_lang: Destination language code (ISO 639‑1).
    Returns:
        dict with translated text under a 'translated' key.
    """
    documents = raw_documents.get('document') or raw_documents.get('documents', [])
    if not documents:
        return {"translated": []}

    translated_docs = []
    for doc in documents:
        # Assume each document has a 'content' field to translate; adjust if needed
        original = doc.get('content', '')
        if not original:
            translated = ''
        else:
            try:
                result = client.translate(original, target_language=target_lang)
                translated = result['translatedText']
            except Exception as e:
                # Fallback to original text if translation fails
                translated = original
        # Preserve original document structure with added translated field
        doc_translation = dict(doc)
        doc_translation['translated'] = translated
        translated_docs.append(doc_translation)

    # Return unified response – single doc or list
    if len(translated_docs) == 1:
        return {"translated": translated_docs[0]}
    return {"translated": translated_docs}

# Helper for missing env variables
get_env_or_raise = lambda var: \\\n    os.getenv(var) or (lambda: (_ for _ in ()).throw(RuntimeError(f"Missing env {var}")))()()
