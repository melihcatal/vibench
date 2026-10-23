import os
import json
from typing import Dict, Any, List, Optional
from datetime import datetime
from bson import ObjectId
from document_models import NormalizedExpense, StorageResult
from document_client import get_mongodb_client


def store_expense_record(
    expense: NormalizedExpense, collection_name: str = "expenses"
) -> StorageResult:
    """
    Persist normalized expense records in MongoDB Atlas.
    """
    try:
        client = get_mongodb_client()

        db = client.get_database("expense_tracker")
        collection = db[collection_name]

        expense_dict = {
            "vendor": expense.vendor,
            "amount": expense.amount,
            "date": expense.date,
            "description": expense.description,
            "category": expense.category.value,
            "subcategory": expense.subcategory,
            "tags": expense.tags,
            "line_items": expense.line_items,
            "source_provider": expense.source_provider,
            "source_model": expense.source_model,
            "confidence_scores": expense.confidence_scores,
            "metadata": expense.metadata,
            "normalization_timestamp": expense.normalization_timestamp,
            "storage_timestamp": datetime.now().isoformat(),
            "status": "pending_review",
        }

        result = collection.insert_one(expense_dict)

        document_id = str(result.inserted_id)

        return StorageResult(
            document_id=document_id,
            storage_location=f"mongodb://{client.address[0]}:{client.address[1]}/expense_tracker.{collection_name}",
            success=True,
            provider="mongodb_atlas",
            metadata={
                "collection": collection_name,
                "database": "expense_tracker",
                "inserted_id": document_id,
            },
        )

    except Exception as e:
        return StorageResult(
            document_id="",
            storage_location="",
            success=False,
            provider="mongodb_atlas",
            metadata={"error": str(e), "collection": collection_name},
        )
