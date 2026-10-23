from google.cloud import translate_v2 as translate
from database_client import NoSQLClient

def translate_document_field(identifier, field, target='en'):
    """Translate a user-facing text field in a stored document."""
    client = NoSQLClient()
    container = client.get_container('my_database', 'my_container')
    item = container.read_item(item={'id': identifier}, partition_key='default')
    payload = item.get('payload')
    if isinstance(payload, dict) and field in payload:
        original = payload[field]
        gclient = translate.Client()
        result = gclient.translate(original, target_language=target)
        # Update payload in place
        payload[field] = result['translatedText']
        # Upsert updated document
        container.replace_item(item=item, partition_key='default')
        return result['translatedText']
    return None
