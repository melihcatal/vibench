import os
import boto3
from google.cloud import translate_v2 as translate
from database_client import NoSQLClient
from database_models import Document

def record_translate(primary_id: str, target_lang: str) -> dict:
    """Translate user-facing fields of a document into the target language.

    This example leverages Google Cloud Translation API. The function loads the
    document from DynamoDB, translates fields listed in TRANSLATABLE_FIELDS,
    and writes back the translated values.
    """
    client = NoSQLClient()
    response = client.get_item(
        TableName=os.getenv('DYNAMODB_TABLE'),
        Key={'id': {'S': primary_id}}
    )
    item = response.get('Item')
    if not item:
        raise ValueError('Document not found')
    doc = Document.from_dict(item)
    TRANSLATABLE_FIELDS = {'title', 'content'}
    translator = translate.Client()
    translated = {}
    for field in TRANSLATABLE_FIELDS:
        if hasattr(doc, field):
            original = getattr(doc, field)
            if not original:
                continue
            # Translate via Google Cloud; you must set GOOGLE_APPLICATION_CREDENTIALS env var
            result = translator.translate(original, target_language=target_lang)
            translated[field] = result['translatedText']
    # Update only the fields that changed
    update_expr = 'SET ' + ', '.join([f"{k} = :{k}" for k in translated])
    expression_values = {f":{k}": {'S': v} for k, v in translated.items()}
    client.update_item(
        TableName=os.getenv('DYNAMODB_TABLE'),
        Key={'id': {'S': primary_id}},
        UpdateExpression=update_expr,
        ExpressionAttributeValues=expression_values
    )
    # Return the merged document with translations
    doc.__dict__.update(translated)
    return doc.to_dict()
