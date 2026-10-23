import os
from database_client import get_client
from database_models import DocumentModel
import google.auth
from google.cloud import translate_v2 as translate

def record_translate(document_id, source_field, target_lang='en'):
    """Translate a text field of a document into a target language using Google Cloud Translation.
    """
    client = get_client()  # placeholder; actual translation client below
    doc = fetch_document(document_id)
    text = doc.data.get(source_field, '')
    if not text:
        return text
    # Use environment variable for credentials (default auth picks up GOOGLE_APPLICATION_CREDENTIALS)
    translate_client = translate.Client()
    result = translate_client.translate(text, target_language=target_lang)
    return result['translatedText']
