from database_client import NoSQLClient

def summarize_documents(identifiers):
    """Summarize a list of retrieved documents into a concise view."""
    client = NoSQLClient()
    container = client.get_container('my_database', 'my_container')
    summaries = []
    for ident in identifiers:
        item = container.read_item(item={'id': ident}, partition_key='default')
        # Simple summary: word count of the payload text field (if exists)
        payload = item.get('payload')
        if isinstance(payload, dict) and 'text' in payload:
            word_count = len(payload['text'].split())
        else:
            word_count = 0
        summaries.append({'id': ident, 'word_count': word_count})
    return summaries
