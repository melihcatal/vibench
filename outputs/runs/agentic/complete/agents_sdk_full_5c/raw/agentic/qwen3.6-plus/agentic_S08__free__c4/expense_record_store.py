"""
[LATER-STEP] Persist normalized expense records in a managed document store.
Uses MongoDB Atlas (pymongo SDK) as the managed cloud document database to store,
retrieve, and query normalized expense records.

Provider: MongoDB Atlas
SDK: pymongo
Connection: mongodb+srv:// (MongoDB Atlas connection string)
"""

import os
import logging
from typing import Optional, Dict, Any, List
from datetime import datetime

from pymongo import MongoClient, errors as pymongo_errors
from pymongo.collection import Collection
from pymongo.database import Database

from document_models import NormalizedExpenseRecord
from document_client import get_mongodb_config, validate_provider_config

logger = logging.getLogger(__name__)

# MongoDB Atlas connection string prefix
MONGODB_ATLAS_HOST_PREFIX = "mongodb+srv://"


class ExpenseRecordStore:
    """
    Manages persistence of normalized expense records in MongoDB Atlas.
    Provides CRUD operations for expense document storage and retrieval.
    """

    def __init__(self, uri: Optional[str] = None, db_name: Optional[str] = None, collection_name: Optional[str] = None):
        """
        Initialize the expense record store with MongoDB Atlas connection.

        Args:
            uri: MongoDB Atlas connection string (mongodb+srv://).
            db_name: Database name (default from config).
            collection_name: Collection name (default from config).
        """
        config = get_mongodb_config()
        self._uri = uri or config.get("uri")
        self._db_name = db_name or config.get("db_name", "expense_documents")
        self._collection_name = collection_name or config.get("collection_name", "expense_records")

        if not self._uri:
            raise ValueError(
                "MongoDB Atlas URI is not configured. "
                "Set MONGODB_URI environment variable with your mongodb+srv:// connection string."
            )

        self._client: Optional[MongoClient] = None
        self._db: Optional[Database] = None
        self._collection: Optional[Collection] = None

    def _connect(self) -> Collection:
        """Establish connection to MongoDB Atlas and return the collection."""
        if self._collection is not None:
            return self._collection

        try:
            logger.info(f"Connecting to MongoDB Atlas: {MONGODB_ATLAS_HOST_PREFIX}***")
            self._client = MongoClient(
                self._uri,
                serverSelectionTimeoutMS=10000,
                connectTimeoutMS=10000,
            )
            # Verify connection with ping
            self._client.admin.command("ping")
            self._db = self._client[self._db_name]
            self._collection = self._db[self._collection_name]

            # Create indexes for efficient querying
            self._collection.create_index("vendor_name")
            self._collection.create_index("transaction_date")
            self._collection.create_index("expense_type")
            self._collection.create_index("document_id", unique=True)

            logger.info(
                f"Connected to MongoDB Atlas collection: "
                f"{self._db_name}.{self._collection_name}"
            )
            return self._collection

        except pymongo_errors.ServerSelectionTimeoutError as e:
            logger.error(f"MongoDB Atlas connection timeout: {str(e)}")
            raise
        except pymongo_errors.ConnectionFailure as e:
            logger.error(f"MongoDB Atlas connection failed: {str(e)}")
            raise

    def store_expense_record(self, record: NormalizedExpenseRecord) -> str:
        """
        Store a normalized expense record in MongoDB Atlas.

        Args:
            record: NormalizedExpenseRecord to persist.

        Returns:
            MongoDB document ID of the stored record.
        """
        collection = self._connect()

        # Convert record to dictionary
        doc = {
            "expense_type": record.expense_type,
            "vendor_name": record.vendor_name,
            "transaction_date": record.transaction_date,
            "total_amount": record.total_amount,
            "currency": record.currency,
            "tax_amount": record.tax_amount,
            "line_items": record.line_items,
            "document_id": record.document_id,
            "source_system": record.source_system,
            "extracted_at": record.extracted_at,
            "validation_status": record.validation_status,
            "stored_at": datetime.utcnow().isoformat(),
        }

        try:
            # Upsert based on document_id to avoid duplicates
            result = collection.update_one(
                {"document_id": record.document_id},
                {"$set": doc},
                upsert=True,
            )

            logger.info(
                f"Stored expense record in MongoDB Atlas: "
                f"vendor={record.vendor_name}, amount={record.total_amount} {record.currency}"
            )
            return str(result.upserted_id) if result.upserted_id else record.document_id

        except pymongo_errors.DuplicateKeyError as e:
            logger.error(f"Duplicate document_id in MongoDB Atlas: {record.document_id}")
            raise

    def get_expense_record(self, document_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve an expense record from MongoDB Atlas by document ID.

        Args:
            document_id: Unique document identifier.

        Returns:
            Expense record dictionary or None if not found.
        """
        collection = self._connect()
        record = collection.find_one({"document_id": document_id})
        if record:
            record.pop("_id", None)
        return record

    def get_expenses_by_vendor(self, vendor_name: str) -> List[Dict[str, Any]]:
        """
        Retrieve all expense records for a specific vendor from MongoDB Atlas.

        Args:
            vendor_name: Vendor name to search for.

        Returns:
            List of expense record dictionaries.
        """
        collection = self._connect()
        records = list(collection.find({"vendor_name": vendor_name}).sort("transaction_date", -1))
        for record in records:
            record.pop("_id", None)
        return records

    def get_expenses_by_date_range(
        self,
        start_date: str,
        end_date: str,
    ) -> List[Dict[str, Any]]:
        """
        Retrieve expense records within a date range from MongoDB Atlas.

        Args:
            start_date: Start date (YYYY-MM-DD).
            end_date: End date (YYYY-MM-DD).

        Returns:
            List of expense record dictionaries.
        """
        collection = self._connect()
        records = list(
            collection.find({
                "transaction_date": {"$gte": start_date, "$lte": end_date}
            }).sort("transaction_date", -1)
        )
        for record in records:
            record.pop("_id", None)
        return records

    def get_total_expenses_by_vendor(self, vendor_name: str) -> float:
        """
        Calculate total expenses for a vendor using MongoDB aggregation.

        Args:
            vendor_name: Vendor name to aggregate.

        Returns:
            Total expense amount.
        """
        collection = self._connect()
        pipeline = [
            {"$match": {"vendor_name": vendor_name}},
            {"$group": {"_id": None, "total": {"$sum": "$total_amount"}}},
        ]
        result = list(collection.aggregate(pipeline))
        return result[0]["total"] if result else 0.0

    def delete_expense_record(self, document_id: str) -> bool:
        """
        Delete an expense record from MongoDB Atlas.

        Args:
            document_id: Document ID to delete.

        Returns:
            True if record was deleted, False otherwise.
        """
        collection = self._connect()
        result = collection.delete_one({"document_id": document_id})
        return result.deleted_count > 0

    def close(self):
        """Close the MongoDB Atlas connection."""
        if self._client:
            self._client.close()
            self._client = None
            self._db = None
            self._collection = None
            logger.info("MongoDB Atlas connection closed")


def store_expense_record(record: NormalizedExpenseRecord) -> str:
    """
    Convenience function to store an expense record in MongoDB Atlas.

    Args:
        record: NormalizedExpenseRecord to persist.

    Returns:
        Document ID of the stored record.
    """
    store = ExpenseRecordStore()
    try:
        return store.store_expense_record(record)
    finally:
        store.close()


def get_expense_record(document_id: str) -> Optional[Dict[str, Any]]:
    """
    Convenience function to retrieve an expense record from MongoDB Atlas.

    Args:
        document_id: Document ID to retrieve.

    Returns:
        Expense record dictionary or None.
    """
    store = ExpenseRecordStore()
    try:
        return store.get_expense_record(document_id)
    finally:
        store.close()
