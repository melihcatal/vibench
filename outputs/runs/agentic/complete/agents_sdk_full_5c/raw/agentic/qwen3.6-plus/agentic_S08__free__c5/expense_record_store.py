"""
Persist normalized expense records in a managed document store using Pinecone.
Provider: Pinecone Vector Database (pinecone.io)
"""

import os
import uuid
import hashlib
import json
from typing import Optional, List, Dict, Any
from pinecone import Pinecone, ServerlessSpec

from document_models import ExpenseRecord, ExpenseStoreResult


def store_expense_record(
    expense: ExpenseRecord,
    api_key: Optional[str] = None,
    environment: Optional[str] = None,
    index_name: Optional[str] = None,
    cloud: str = "aws",
    region: str = "us-east-1",
    dimension: int = 768,
    metadata_fields: Optional[Dict[str, Any]] = None,
) -> ExpenseStoreResult:
    """
    Persist a normalized expense record in Pinecone vector database.
    
    Uses Pinecone (api.pinecone.io) to store expense records as vector embeddings
    with metadata for semantic search and retrieval. Records are indexed by
    vendor, date, amount, and document type for efficient querying.
    
    Args:
        expense: ExpenseRecord to persist
        api_key: Pinecone API key
        environment: Pinecone environment/region
        index_name: Name of the Pinecone index (default: expense-records)
        cloud: Cloud provider for serverless spec (default: aws)
        region: Cloud region for serverless spec (default: us-east-1)
        dimension: Vector embedding dimension (default: 768)
        metadata_fields: Additional metadata to store with the record
    
    Returns:
        ExpenseStoreResult with storage confirmation and record ID
    """
    pc_api_key = api_key or os.environ.get("PINECONE_API_KEY", "")
    pc_env = environment or os.environ.get("PINECONE_ENVIRONMENT", "")
    idx_name = index_name or os.environ.get("PINECONE_INDEX_NAME", "expense-records")
    
    if not pc_api_key:
        raise ValueError("Pinecone API key must be provided via parameter or PINECONE_API_KEY env var")
    
    pc = Pinecone(api_key=pc_api_key)
    
    _ensure_index_exists(pc, idx_name, dimension, cloud, region)
    
    index = pc.Index(idx_name)
    
    record_id = str(uuid.uuid4())
    vector_id = hashlib.sha256(record_id.encode()).hexdigest()[:16]
    
    metadata = _build_expense_metadata(expense, metadata_fields)
    
    embedding = _generate_expense_embedding(expense, dimension)
    
    index.upsert(
        vectors=[{
            "id": vector_id,
            "values": embedding,
            "metadata": metadata,
        }]
    )
    
    return ExpenseStoreResult(
        record_id=record_id,
        stored=True,
        vector_id=vector_id,
        index_name=idx_name,
    )


def store_expense_records_batch(
    expenses: List[ExpenseRecord],
    api_key: Optional[str] = None,
    environment: Optional[str] = None,
    index_name: Optional[str] = None,
    cloud: str = "aws",
    region: str = "us-east-1",
    dimension: int = 768,
) -> List[ExpenseStoreResult]:
    """
    Persist multiple expense records in Pinecone in a single batch operation.
    
    Args:
        expenses: List of ExpenseRecord objects to persist
        api_key: Pinecone API key
        environment: Pinecone environment
        index_name: Name of the Pinecone index
        cloud: Cloud provider
        region: Cloud region
        dimension: Vector embedding dimension
    
    Returns:
        List of ExpenseStoreResult objects
    """
    pc_api_key = api_key or os.environ.get("PINECONE_API_KEY", "")
    pc_env = environment or os.environ.get("PINECONE_ENVIRONMENT", "")
    idx_name = index_name or os.environ.get("PINECONE_INDEX_NAME", "expense-records")
    
    if not pc_api_key:
        raise ValueError("Pinecone API key must be provided")
    
    pc = Pinecone(api_key=pc_api_key)
    _ensure_index_exists(pc, idx_name, dimension, cloud, region)
    
    index = pc.Index(idx_name)
    
    vectors_to_upsert = []
    results: List[ExpenseStoreResult] = []
    
    for expense in expenses:
        record_id = str(uuid.uuid4())
        vector_id = hashlib.sha256(record_id.encode()).hexdigest()[:16]
        metadata = _build_expense_metadata(expense)
        embedding = _generate_expense_embedding(expense, dimension)
        
        vectors_to_upsert.append({
            "id": vector_id,
            "values": embedding,
            "metadata": metadata,
        })
        
        results.append(
            ExpenseStoreResult(
                record_id=record_id,
                stored=True,
                vector_id=vector_id,
                index_name=idx_name,
            )
        )
    
    if vectors_to_upsert:
        index.upsert(vectors=vectors_to_upsert)
    
    return results


def query_expense_records(
    query_text: str,
    top_k: int = 5,
    api_key: Optional[str] = None,
    index_name: Optional[str] = None,
    dimension: int = 768,
    filter_criteria: Optional[Dict[str, Any]] = None,
) -> List[Dict[str, Any]]:
    """
    Query stored expense records in Pinecone using semantic similarity.
    
    Args:
        query_text: Natural language query for expense records
        top_k: Number of results to return
        api_key: Pinecone API key
        index_name: Name of the Pinecone index
        dimension: Vector embedding dimension
        filter_criteria: Optional metadata filters (e.g., {"vendor": "ABC Corp"})
    
    Returns:
        List of matching expense record metadata
    """
    pc_api_key = api_key or os.environ.get("PINECONE_API_KEY", "")
    idx_name = index_name or os.environ.get("PINECONE_INDEX_NAME", "expense-records")
    
    if not pc_api_key:
        raise ValueError("Pinecone API key must be provided")
    
    pc = Pinecone(api_key=pc_api_key)
    index = pc.Index(idx_name)
    
    query_embedding = _generate_query_embedding(query_text, dimension)
    
    kwargs: Dict[str, Any] = {
        "vector": query_embedding,
        "top_k": top_k,
        "include_metadata": True,
    }
    
    if filter_criteria:
        kwargs["filter"] = filter_criteria
    
    response = index.query(**kwargs)
    
    results = []
    for match in response.get("matches", []):
        results.append({
            "id": match.get("id"),
            "score": match.get("score"),
            "metadata": match.get("metadata", {}),
        })
    
    return results


def _ensure_index_exists(
    pc: Pinecone,
    index_name: str,
    dimension: int,
    cloud: str,
    region: str,
) -> None:
    """Create the Pinecone index if it does not already exist."""
    existing_indexes = pc.list_indexes().names()
    
    if index_name not in existing_indexes:
        pc.create_index(
            name=index_name,
            dimension=dimension,
            metric="cosine",
            spec=ServerlessSpec(
                cloud=cloud,
                region=region,
            ),
        )
        
        import time
        for _ in range(60):
            if index_name in pc.list_indexes().names():
                break
            time.sleep(1)


def _build_expense_metadata(
    expense: ExpenseRecord,
    additional: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Build Pinecone metadata dictionary from an ExpenseRecord."""
    metadata: Dict[str, Any] = {
        "vendor": expense.vendor or "",
        "date": expense.date or "",
        "total_amount": expense.total_amount or 0.0,
        "tax_amount": expense.tax_amount or 0.0,
        "currency": expense.currency,
        "document_type": expense.document_type,
        "line_item_count": len(expense.line_items),
    }
    
    line_item_descriptions = []
    for item in expense.line_items:
        if item.description:
            line_item_descriptions.append(item.description)
    metadata["line_item_descriptions"] = json.dumps(line_item_descriptions)
    
    if additional:
        metadata.update(additional)
    
    metadata.update(expense.metadata)
    
    return metadata


def _generate_expense_embedding(expense: ExpenseRecord, dimension: int) -> List[float]:
    """
    Generate a deterministic embedding vector from an expense record.
    
    In production, this would use a real embedding model (e.g., OpenAI text-embedding-ada-002
    or AWS Bedrock Titan Embeddings). Here we create a reproducible hash-based vector.
    """
    embedding_text = " ".join(filter(None, [
        str(expense.vendor),
        str(expense.date),
        str(expense.total_amount),
        expense.document_type,
        expense.currency,
        " ".join(
            item.description or ""
            for item in expense.line_items
            if item.description
        ),
    ]))
    
    hash_bytes = hashlib.sha256(embedding_text.encode("utf-8")).digest()
    
    embedding: List[float] = []
    for i in range(dimension):
        byte_val = hash_bytes[i % len(hash_bytes)]
        normalized = (byte_val / 255.0) * 2 - 1
        embedding.append(round(normalized, 6))
    
    magnitude = sum(v * v for v in embedding) ** 0.5
    if magnitude > 0:
        embedding = [v / magnitude for v in embedding]
    
    return embedding


def _generate_query_embedding(query_text: str, dimension: int) -> List[float]:
    """
    Generate a deterministic embedding vector from query text.
    
    Uses the same hashing approach as _generate_expense_embedding for consistency.
    """
    hash_bytes = hashlib.sha256(query_text.encode("utf-8")).digest()
    
    embedding: List[float] = []
    for i in range(dimension):
        byte_val = hash_bytes[i % len(hash_bytes)]
        normalized = (byte_val / 255.0) * 2 - 1
        embedding.append(round(normalized, 6))
    
    magnitude = sum(v * v for v in embedding) ** 0.5
    if magnitude > 0:
        embedding = [v / magnitude for v in embedding]
    
    return embedding


if __name__ == "__main__":
    sample_expense = ExpenseRecord(
        vendor="Office Supply Co.",
        date="2024-01-15",
        total_amount=250.00,
        tax_amount=20.00,
        currency="USD",
        document_type="invoice",
        metadata={"invoice_number": "INV-2024-001"},
    )
    
    try:
        result = store_expense_record(sample_expense)
        print(result.model_dump_json(indent=2))
    except ValueError as e:
        print(f"Skipping store demo (no API key): {e}")
