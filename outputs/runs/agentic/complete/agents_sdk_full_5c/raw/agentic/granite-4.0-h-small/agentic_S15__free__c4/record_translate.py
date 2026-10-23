# [LATER-STEP] record_translate.py
import os
import json
from google.cloud import translate_v2 as translate
from database_client import NoSQLClient
from database_models import denormalize_document, normalize_document

def translate_document_fields(doc_id, fields, target_lang='es'):
    """Translate specified string fields of a document into a target language.

    Args:
        doc_id (str): Primary identifier of the document.
        fields (list): List of field names to translate.
        target_lang (str): ISO 639-1 language code (default: Spanish).
    Returns:
        dict: Updated document with translated field values.
    """
    client = NoSQLClient()
    item = client.get_item(TableName=client.table_name, Key={'id': {'S': doc_id}})
    raw = item.get('Item', {})
    if not raw:
        raise ValueError(f"Document {doc_id} not found")
    doc = denormalize_document(json.loads(raw.get('content', '{}')))
    translate_client = translate.Client()
    for field in fields:
        if field in doc and isinstance(doc[field], str):
            result = translate_client.translate(doc[field], target_language=target_lang)
            doc[field] = result['translatedText']
    # Persist the updated document back to DynamoDB (upsert)
    payload = normalize_document(doc)
    client.put_item(TableName=client.table_name,
                    Key={'id': {'S': doc_id}},
                    Item={'content': {'S': json.dumps(payload)}})
    print(f"Translated fields {fields} for document {doc_id} into {target_lang}.")
    return doc