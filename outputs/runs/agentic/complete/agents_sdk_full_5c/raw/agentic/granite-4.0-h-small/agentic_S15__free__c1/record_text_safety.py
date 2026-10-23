import os
import re
from database_client import NoSQLClient
from database_models import Document

def record_text_safety(primary_id: str, field: str = 'content') -> bool:
    """Check a document field for unsafe text patterns (e.g., SQL injection, XSS).

    This naive implementation scans the field value for common unsafe characters
    and blocks the operation if found. In production you would integrate a
    dedicated content safety service (e.g., Google Cloud Content Safety).
    """
    # Load the document
    client = NoSQLClient()
    response = client.get_item(
        TableName=os.getenv('DYNAMODB_TABLE'),
        Key={'id': {'S': primary_id}}
    )
    item = response.get('Item')
    if not item:
        raise ValueError('Document not found')
    content = Document.from_dict(item).get(field)
    if not isinstance(content, str):
        return True  # non-text fields are considered safe
    # Simple detection patterns
    unsafe_patterns = [
        re.compile(r"--"),                # SQL comment
        re.compile(r"<script>"),          # XSS script tag
        re.compile(r"%27"),              # URL-encoded single quote
        re.compile(r"'|"""),             # Single/double quote
    ]
    for pattern in unsafe_patterns:
        if pattern.search(content):
            return False
    return True
