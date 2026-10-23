import os
from typing import Dict, Any, List, Optional
from datetime import datetime
from google.cloud import firestore
from google.cloud.firestore_v1.base_query import FieldFilter


class ExpenseRecordStore:
    """Persist normalized expense records in Google Cloud Firestore."""

    def __init__(self, collection_name: str = "expense_records"):
        credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        if not credentials_path or not os.path.exists(credentials_path):
            raise ValueError(
                "Google Cloud credentials not configured or file not found"
            )

        self.db = firestore.Client()
        self.collection = self.db.collection(collection_name)

    def store_expense(self, expense_data: Dict[str, Any]) -> str:
        """
        Store a single expense record in Firestore.
        Returns the document ID.
        """
        if "expense_id" not in expense_data:
            expense_data["expense_id"] = (
                f"exp_{int(datetime.now().timestamp())}_{os.urandom(4).hex()}"
            )

        expense_data["created_at"] = firestore.SERVER_TIMESTAMP
        expense_data["updated_at"] = firestore.SERVER_TIMESTAMP

        doc_ref = self.collection.document(expense_data["expense_id"])
        doc_ref.set(expense_data)

        return doc_ref.id

    def batch_store_expenses(self, expenses: List[Dict[str, Any]]) -> List[str]:
        """
        Store multiple expense records in a batch.
        Returns list of document IDs.
        """
        batch = self.db.batch()
        doc_ids = []

        for expense in expenses:
            if "expense_id" not in expense:
                expense["expense_id"] = (
                    f"exp_{int(datetime.now().timestamp())}_{os.urandom(4).hex()}"
                )

            expense["created_at"] = firestore.SERVER_TIMESTAMP
            expense["updated_at"] = firestore.SERVER_TIMESTAMP

            doc_ref = self.collection.document(expense["expense_id"])
            batch.set(doc_ref, expense)
            doc_ids.append(doc_ref.id)

        batch.commit()
        return doc_ids

    def get_expense(self, expense_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve an expense record by ID.
        """
        doc_ref = self.collection.document(expense_id)
        doc = doc_ref.get()

        if doc.exists:
            data = doc.to_dict()
            data["firestore_id"] = doc.id
            return data
        return None

    def query_expenses(
        self, filters: Dict[str, Any] = None, limit: int = 100
    ) -> List[Dict[str, Any]]:
        """
        Query expense records with optional filters.
        """
        query = self.collection

        if filters:
            for field, value in filters.items():
                if isinstance(value, (list, tuple)) and len(value) == 2:
                    op, val = value
                    if op == "==":
                        query = query.where(filter=FieldFilter(field, "==", val))
                    elif op == ">":
                        query = query.where(filter=FieldFilter(field, ">", val))
                    elif op == "<":
                        query = query.where(filter=FieldFilter(field, "<", val))
                    elif op == ">=":
                        query = query.where(filter=FieldFilter(field, ">=", val))
                    elif op == "<=":
                        query = query.where(filter=FieldFilter(field, "<=", val))
                else:
                    query = query.where(filter=FieldFilter(field, "==", value))

        query = query.limit(limit)
        results = query.stream()

        expenses = []
        for doc in results:
            data = doc.to_dict()
            data["firestore_id"] = doc.id
            expenses.append(data)

        return expenses

    def update_expense(self, expense_id: str, updates: Dict[str, Any]) -> bool:
        """
        Update an existing expense record.
        """
        updates["updated_at"] = firestore.SERVER_TIMESTAMP

        doc_ref = self.collection.document(expense_id)
        doc = doc_ref.get()

        if not doc.exists:
            return False

        doc_ref.update(updates)
        return True

    def delete_expense(self, expense_id: str) -> bool:
        """
        Delete an expense record.
        """
        doc_ref = self.collection.document(expense_id)
        doc = doc_ref.get()

        if not doc.exists:
            return False

        doc_ref.delete()
        return True

    def get_collection_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the expense records collection.
        """
        total_count = 0
        by_source_type = {}
        total_amount = 0.0

        docs = self.collection.limit(1000).stream()

        for doc in docs:
            total_count += 1
            data = doc.to_dict()

            source_type = data.get("source_type", "unknown")
            by_source_type[source_type] = by_source_type.get(source_type, 0) + 1

            total_amount += data.get("total_amount", 0.0)

        return {
            "total_records": total_count,
            "by_source_type": by_source_type,
            "total_amount": total_amount,
            "average_amount": total_amount / total_count if total_count > 0 else 0.0,
        }
