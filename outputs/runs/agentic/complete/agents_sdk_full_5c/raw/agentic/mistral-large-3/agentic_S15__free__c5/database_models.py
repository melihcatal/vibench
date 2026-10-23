from pydantic import BaseModel
from typing import Dict, Any, Optional

class DocumentRequest(BaseModel):
    """
    Defines the structure for document upsert requests in Azure Cosmos DB.
    """
    id: str
    partitionKey: str
    [key: str]: Any

class DocumentResponse(BaseModel):
    """
    Defines the structure for document fetch responses from Azure Cosmos DB.
    """
    id: str
    partitionKey: str
    _etag: Optional[str] = None
    [key: str]: Any