import os
import json
from typing import Dict, List, Any, Optional
from datetime import datetime
from document_models import ExpenseRecord, NormalizedExpense
from document_client import get_document_client


def store_expense_record(expense_record: Dict[str, Any]) -> Dict[str, Any]:
    """
    Persist normalized expense records in Pinecone vector database.
    """
    import pinecone
    from pinecone import Pinecone, ServerlessSpec

    # Initialize Pinecone client
    api_key = os.getenv("PINECONE_API_KEY")
    environment = os.getenv("PINECONE_ENVIRONMENT")

    if not api_key or not environment:
        raise ValueError("Pinecone API key and environment must be configured")

    pc = Pinecone(api_key=api_key)

    # Use or create index
    index_name = "expense-records"

    storage_results = {
        "stored": False,
        "record_id": None,
        "index_name": index_name,
        "provider": "pinecone",
        "storage_timestamp": datetime.utcnow().isoformat(),
        "vector_dimension": 1536,  # OpenAI embedding dimension
    }

    try:
        # Check if index exists, create if not
        if index_name not in pc.list_indexes().names():
            pc.create_index(
                name=index_name,
                dimension=1536,
                metric="cosine",
                spec=ServerlessSpec(cloud="aws", region="us-east-1"),
            )

        # Connect to index
        index = pc.Index(index_name)

        # Generate embedding for the expense record
        # Use OpenAI to generate embedding
        from openai import OpenAI

        openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        # Create text for embedding
        expense_text = f"""
        Vendor: {expense_record.get("vendor_name", "Unknown")}
        Date: {expense_record.get("transaction_date", "Unknown")}
        Amount: {expense_record.get("total_amount", 0)} {expense_record.get("currency", "USD")}
        Category: {expense_record.get("category", "other")}
        Payment Method: {expense_record.get("payment_method", "credit_card")}
        Notes: {expense_record.get("notes", "")}
        """

        # Generate embedding
        embedding_response = openai_client.embeddings.create(
            model="text-embedding-3-small", input=expense_text
        )

        embedding = embedding_response.data[0].embedding

        # Create unique ID for the record
        record_id = f"expense_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{hash(json.dumps(expense_record)) % 10000}"

        # Prepare metadata
        metadata = {
            "vendor_name": expense_record.get("vendor_name"),
            "transaction_date": expense_record.get("transaction_date"),
            "total_amount": expense_record.get("total_amount"),
            "currency": expense_record.get("currency", "USD"),
            "category": expense_record.get("category", "other"),
            "payment_method": expense_record.get("payment_method", "credit_card"),
            "original_document_type": expense_record.get("metadata", {}).get(
                "original_document_type", "unknown"
            ),
            "normalization_provider": expense_record.get("metadata", {}).get(
                "normalization_provider", "unknown"
            ),
            "normalization_model": expense_record.get("metadata", {}).get(
                "normalization_model", "unknown"
            ),
            "storage_timestamp": storage_results["storage_timestamp"],
        }

        # Add line items summary if available
        if "line_items" in expense_record and expense_record["line_items"]:
            metadata["line_item_count"] = len(expense_record["line_items"])
            metadata["line_items_summary"] = json.dumps(
                [
                    {
                        "description": item.get("description"),
                        "amount": item.get("amount"),
                    }
                    for item in expense_record["line_items"][:3]  # First 3 items
                ]
            )

        # Store in Pinecone
        index.upsert(
            vectors=[{"id": record_id, "values": embedding, "metadata": metadata}]
        )

        storage_results["stored"] = True
        storage_results["record_id"] = record_id
        storage_results["embedding_dimension"] = len(embedding)

        # Get index stats
        index_stats = index.describe_index_stats()
        storage_results["index_stats"] = {
            "total_vectors": index_stats.total_vector_count,
            "dimension": index_stats.dimension,
            "index_fullness": index_stats.index_fullness,
        }

        # Also store full record in metadata for retrieval
        full_record_key = f"full_record_{record_id}"
        index.upsert(
            vectors=[
                {
                    "id": full_record_key,
                    "values": [0.0] * 1536,  # Dummy embedding
                    "metadata": {
                        "expense_record": json.dumps(expense_record),
                        "record_type": "full_record",
                        "linked_record_id": record_id,
                    },
                }
            ]
        )

        # Create expense record in normalized form
        normalized_expense = NormalizedExpense(
            expense=ExpenseRecord(**expense_record),
            normalization_provider=expense_record.get("metadata", {}).get(
                "normalization_provider", "unknown"
            ),
            normalization_model=expense_record.get("metadata", {}).get(
                "normalization_model", "unknown"
            ),
            original_document_type=expense_record.get("metadata", {}).get(
                "original_document_type", "unknown"
            ),
            confidence_score=expense_record.get("metadata", {}).get("confidence", 1.0),
            validation_status="stored",
        )

        storage_results["normalized_expense"] = normalized_expense.dict()

    except Exception as e:
        storage_results["error"] = str(e)
        storage_results["stored"] = False

    return storage_results


def search_similar_expenses(query: str, top_k: int = 5) -> List[Dict[str, Any]]:
    """
    Search for similar expense records in Pinecone.
    """
    import pinecone
    from openai import OpenAI

    api_key = os.getenv("PINECONE_API_KEY")
    pc = pinecone.Pinecone(api_key=api_key)

    index_name = "expense-records"

    if index_name not in pc.list_indexes().names():
        return []

    index = pc.Index(index_name)

    # Generate embedding for query
    openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    embedding_response = openai_client.embeddings.create(
        model="text-embedding-3-small", input=query
    )

    query_embedding = embedding_response.data[0].embedding

    # Search in Pinecone
    search_results = index.query(
        vector=query_embedding, top_k=top_k, include_metadata=True
    )

    results = []
    for match in search_results.matches:
        result = {
            "record_id": match.id,
            "score": match.score,
            "metadata": match.metadata,
        }

        # Try to get full record if available
        if "linked_record_id" in match.metadata:
            full_record_id = f"full_record_{match.metadata['linked_record_id']}"
            try:
                fetch_result = index.fetch(ids=[full_record_id])
                if full_record_id in fetch_result.vectors:
                    full_metadata = fetch_result.vectors[full_record_id].metadata
                    if "expense_record" in full_metadata:
                        result["full_record"] = json.loads(
                            full_metadata["expense_record"]
                        )
            except:
                pass

        results.append(result)

    return results
