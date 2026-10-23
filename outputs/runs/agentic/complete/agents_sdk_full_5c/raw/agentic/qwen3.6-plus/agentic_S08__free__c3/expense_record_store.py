"""Persist normalized expense records in a managed document store using Pinecone vector database."""

import os
import json
import hashlib
import uuid
from typing import Optional
from pinecone import Pinecone
from document_models import NormalizedExpenseRecord


def store_expense_record(record: NormalizedExpenseRecord, metadata_extra: Optional[dict] = None) -> dict:
    """Persist a normalized expense record in Pinecone managed vector document store.

    Uses Pinecone (api.pinecone.io) to store expense records as vector embeddings with
    structured metadata for retrieval and querying.
    """
    api_key = os.environ.get("PINECONE_API_KEY", "")
    index_name = os.environ.get("PINECONE_INDEX_NAME", "expense-records")
    environment = os.environ.get("PINECONE_ENVIRONMENT", "us-east1-gcp")

    pc = Pinecone(api_key=api_key)
    index = pc.Index(index_name)

    record_dict = record.to_dict()
    record_id = record_dict.get("document_id") or hashlib.sha256(
        json.dumps(record_dict, sort_keys=True, default=str).encode()
    ).hexdigest()[:16]

    text_representation = _build_text_embedding_input(record)
    embedding = _generate_embedding(text_representation)

    metadata = {
        "vendor_name": record.vendor_name,
        "expense_type": record.expense_type,
        "document_date": record.document_date or "",
        "currency": record.currency,
        "total_amount": record.total_amount or 0.0,
        "tax_amount": record.tax_amount or 0.0,
        "subtotal": record.subtotal or 0.0,
        "confidence": record.confidence,
        "source_provider": record.source_provider,
        "record_id": record_id,
    }
    if metadata_extra:
        metadata.update(metadata_extra)

    index.upsert(
        vectors=[{
            "id": record_id,
            "values": embedding,
            "metadata": metadata,
        }]
    )

    return {
        "status": "stored",
        "record_id": record_id,
        "vendor": record.vendor_name,
        "total_amount": record.total_amount,
        "provider": "pinecone",
        "index": index_name,
        "embedding_dimensions": len(embedding),
    }


def store_expense_records(records: list[NormalizedExpenseRecord]) -> list[dict]:
    """Batch persist multiple normalized expense records in Pinecone."""
    api_key = os.environ.get("PINECONE_API_KEY", "")
    index_name = os.environ.get("PINECONE_INDEX_NAME", "expense-records")

    pc = Pinecone(api_key=api_key)
    index = pc.Index(index_name)

    vectors_to_upsert = []
    results = []

    for record in records:
        record_dict = record.to_dict()
        record_id = record_dict.get("document_id") or str(uuid.uuid4())

        text_representation = _build_text_embedding_input(record)
        embedding = _generate_embedding(text_representation)

        metadata = {
            "vendor_name": record.vendor_name,
            "expense_type": record.expense_type,
            "document_date": record.document_date or "",
            "currency": record.currency,
            "total_amount": record.total_amount or 0.0,
            "tax_amount": record.tax_amount or 0.0,
            "subtotal": record.subtotal or 0.0,
            "confidence": record.confidence,
            "source_provider": record.source_provider,
            "record_id": record_id,
        }

        vectors_to_upsert.append({
            "id": record_id,
            "values": embedding,
            "metadata": metadata,
        })

        results.append({
            "status": "queued",
            "record_id": record_id,
            "vendor": record.vendor_name,
            "total_amount": record.total_amount,
        })

    if vectors_to_upsert:
        index.upsert(vectors=vectors_to_upsert)
        for result in results:
            result["status"] = "stored"

    return results


def query_expense_records(
    query_text: str,
    vendor_filter: Optional[str] = None,
    min_amount: Optional[float] = None,
    top_k: int = 10,
) -> list[dict]:
    """Query stored expense records from Pinecone document store.

    Uses Pinecone vector similarity search (api.pinecone.io) to find relevant
    expense records based on semantic query.
    """
    api_key = os.environ.get("PINECONE_API_KEY", "")
    index_name = os.environ.get("PINECONE_INDEX_NAME", "expense-records")

    pc = Pinecone(api_key=api_key)
    index = pc.Index(index_name)

    query_embedding = _generate_embedding(query_text)

    filter_dict = {}
    if vendor_filter:
        filter_dict["vendor_name"] = {"$eq": vendor_filter}
    if min_amount is not None:
        filter_dict["total_amount"] = {"$gte": min_amount}

    query_params = {
        "vector": query_embedding,
        "top_k": top_k,
        "include_metadata": True,
    }
    if filter_dict:
        query_params["filter"] = filter_dict

    response = index.query(**query_params)

    return [
        {
            "record_id": match["id"],
            "score": match["score"],
            "metadata": match["metadata"],
        }
        for match in response.get("matches", [])
    ]


def retrieve_expense_record(record_id: str) -> Optional[dict]:
    """Retrieve a specific expense record from Pinecone by ID."""
    api_key = os.environ.get("PINECONE_API_KEY", "")
    index_name = os.environ.get("PINECONE_INDEX_NAME", "expense-records")

    pc = Pinecone(api_key=api_key)
    index = pc.Index(index_name)

    response = index.fetch(ids=[record_id])
    if record_id in response.get("vectors", {}):
        vector_data = response["vectors"][record_id]
        return {
            "record_id": record_id,
            "metadata": vector_data.get("metadata", {}),
            "provider": "pinecone",
        }
    return None


def _build_text_embedding_input(record: NormalizedExpenseRecord) -> str:
    """Build a text representation of the expense record for embedding."""
    parts = [
        f"Vendor: {record.vendor_name}",
        f"Type: {record.expense_type}",
        f"Date: {record.document_date}",
        f"Currency: {record.currency}",
        f"Total: {record.total_amount}",
        f"Tax: {record.tax_amount}",
    ]
    for item in record.line_items:
        desc = item.get("description", "")
        if desc:
            parts.append(f"Item: {desc}")
    return " ".join(parts)


def _generate_embedding(text: str) -> list[float]:
    """Generate an embedding vector for the given text using OpenAI embeddings via Pinecone integration."""
    import openai

    api_key = os.environ.get("OPENAI_API_KEY", "")
    client = openai.OpenAI(api_key=api_key)

    response = client.embeddings.create(
        input=text,
        model="text-embedding-3-small",
    )

    return response.data[0].embedding


if __name__ == "__main__":
    sample_record = NormalizedExpenseRecord(
        expense_type="invoice",
        vendor_name="Acme Corp",
        document_date="2024-01-15",
        currency="USD",
        total_amount=1250.00,
        tax_amount=125.00,
        subtotal=1125.00,
        confidence=0.95,
        source_provider="openai_normalized",
    )
    result = store_expense_record(sample_record)
    print(json.dumps(result, indent=2))
