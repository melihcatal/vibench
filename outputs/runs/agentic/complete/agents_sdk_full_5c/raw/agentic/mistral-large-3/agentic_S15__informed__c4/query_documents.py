from typing import List, Dict, Any, Optional
from database_client import MongoDBClient
from database_models import QueryRequest, DocumentResponse, normalize_document

client = MongoDBClient()
collection = client.get_collection()

def query_documents(field_name: str, field_value: Any, partition_key: Optional[str] = None) -> List[DocumentResponse]:
    """Query documents in MongoDB Atlas by a field value or partition key."""
    query = {field_name: field_value}
    if partition_key:
        query["partition_key"] = partition_key
    
    documents = collection.find(query)
    return [normalize_document(doc) for doc in documents]