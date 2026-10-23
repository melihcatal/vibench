from database_client import NoSQLClient
from database_models import Document

def record_summary(primary_id: str) -> dict:
    """Retrieve a document and return a concise summary suitable for UI display.

    Summary includes id, created_at, title (if present) and a truncated content
    preview (first 200 characters). Uses DynamoDB as the backend.
    """
    client = NoSQLClient()
    response = client.get_item(
        TableName=os.getenv('DYNAMODB_TABLE'),
        Key={'id': {'S': primary_id}}
    )
    item = response.get('Item')
    if not item:
        return {}
    doc = Document.from_dict(item)
    summary = {'id': doc.id}
    if hasattr(doc, 'created_at'):
        summary['created_at'] = doc.created_at
    if hasattr(doc, 'title'):
        summary['title'] = doc.title
    if hasattr(doc, 'content'):
        summary['content_preview'] = str(doc.content)[:200] + ('...' if len(doc.content) > 200 else '')
    return summary
