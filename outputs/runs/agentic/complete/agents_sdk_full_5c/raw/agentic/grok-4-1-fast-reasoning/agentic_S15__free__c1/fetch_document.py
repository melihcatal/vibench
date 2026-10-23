import os
from typing import Dict, Any, Optional
from database_client import get_table
from database_models import Document, FetchResponse

def fetch_document(identifier: str) -> FetchResponse:
    table = get_table()
    response = table.get_item(Key={'id': identifier})
    return response.get('Item')
