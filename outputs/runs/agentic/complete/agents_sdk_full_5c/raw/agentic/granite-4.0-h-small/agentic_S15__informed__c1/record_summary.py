import os
from database_client import get_dynamodb_client
from database_models import Document

# Managed NoSQL store: Amazon DynamoDB

def summarize_documents(doc_ids: list[str]) -> dict:
    """Fetch a list of documents and return a concise summary for each.

    Returns a dict mapping doc_id -> {title, version, length, safe}.
    The 'safe' flag can be filled in by record_text_safety later.
    """
    client = get_dynamodb_client()
    summaries = {}
    for doc_id in doc_ids:
        response = client.get_item(
            TableName=os.getenv('DYNAMODB_TABLE'),
            Key={'id': {'S': doc_id}}
        )
        item = response.get('Item')
        if item:
            doc = Document.from_dynamodb_item(item)
            summaries[doc_id] = {
                'title': doc.title,
                'version': doc.version,
                'length': len(doc.content)
            }
        else:
            summaries[doc_id] = {'error': f'Document {doc_id} not found'}
    return summaries

if __name__ == "__main__":
    # Example summarization for demo docs
    summary = summarize_documents(['demo-1', 'demo-2'])
    print('Summaries:', summary)
