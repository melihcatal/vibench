import re
from database_client import NoSQLClient

def safe_text(text):
    """Check a user-generated text field for unsafe content.

    Simple heuristic: reject text containing certain profanity.
    Real implementation would use a managed content moderation service.
    """
    profanity_list = ['badword1', 'badword2', 'badword3']
    return not any(word in text.lower() for word in profanity_list)

def check_document_safety(identifier):
    client = NoSQLClient()
    container = client.get_container('my_database', 'my_container')
    item = container.read_item(item={'id': identifier}, partition_key='default')
    payload = item.get('payload')
    if isinstance(payload, dict) and 'text' in payload:
        return safe_text(payload['text'])
    return True
