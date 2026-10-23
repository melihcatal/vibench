import os
import json
from typing import Dict, Any, List, Optional
from datetime import datetime
from pymongo import MongoClient
from pymongo.errors import PyMongoError


class ExpenseRecordStore:
    def __init__(self):
        self.connection_string = os.getenv("MONGODB_ATLAS_URI")

        if not self.connection_string:
            raise ValueError("MongoDB Atlas connection string not configured")

        self.client = MongoClient(self.connection_string)
        self.db = self.client.get_database("expense_tracker")
        self.collection = self.db.expense_records

        self._ensure_indexes()

    def _ensure_indexes(self):
        self.collection.create_index("expense_id", unique=True)
        self.collection.create_index("vendor")
        self.collection.create_index("date")
        self.collection.create_index([("vendor", 1), ("date", -1)])
        self.collection.create_index("source_document_id")

    def store_expense_record(self, expense_record: Dict[str, Any]) -> Dict[str, Any]:
        try:
            record_with_metadata = {
                **expense_record,
                "stored_at": datetime.utcnow(),
                "updated_at": datetime.utcnow(),
                "storage_provider": "mongodb_atlas",
            }

            result = self.collection.insert_one(record_with_metadata)

            return {
                "success": True,
                "expense_id": expense_record.get("expense_id"),
                "mongodb_id": str(result.inserted_id),
                "provider": "mongodb_atlas",
                "database": "expense_tracker",
                "collection": "expense_records",
            }

        except PyMongoError as e:
            return {
                "success": False,
                "error": str(e),
                "expense_id": expense_record.get("expense_id"),
                "provider": "mongodb_atlas",
            }

    def batch_store_expense_records(
        self, expense_records: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        try:
            records_with_metadata = []
            for record in expense_records:
                records_with_metadata.append(
                    {
                        **record,
                        "stored_at": datetime.utcnow(),
                        "updated_at": datetime.utcnow(),
                        "storage_provider": "mongodb_atlas",
                    }
                )

            result = self.collection.insert_many(records_with_metadata)

            return {
                "success": True,
                "count_inserted": len(result.inserted_ids),
                "inserted_ids": [str(id) for id in result.inserted_ids],
                "provider": "mongodb_atlas",
                "database": "expense_tracker",
                "collection": "expense_records",
            }

        except PyMongoError as e:
            return {
                "success": False,
                "error": str(e),
                "count_attempted": len(expense_records),
                "provider": "mongodb_atlas",
            }

    def get_expense_record(self, expense_id: str) -> Optional[Dict[str, Any]]:
        try:
            record = self.collection.find_one({"expense_id": expense_id})

            if record:
                record["_id"] = str(record["_id"])
                return record
            else:
                return None

        except PyMongoError as e:
            raise Exception(f"MongoDB error: {str(e)}")

    def update_expense_record(
        self, expense_id: str, updates: Dict[str, Any]
    ) -> Dict[str, Any]:
        try:
            updates["updated_at"] = datetime.utcnow()

            result = self.collection.update_one(
                {"expense_id": expense_id}, {"$set": updates}
            )

            return {
                "success": result.modified_count > 0,
                "expense_id": expense_id,
                "matched_count": result.matched_count,
                "modified_count": result.modified_count,
                "provider": "mongodb_atlas",
            }

        except PyMongoError as e:
            return {
                "success": False,
                "error": str(e),
                "expense_id": expense_id,
                "provider": "mongodb_atlas",
            }

    def delete_expense_record(self, expense_id: str) -> Dict[str, Any]:
        try:
            result = self.collection.delete_one({"expense_id": expense_id})

            return {
                "success": result.deleted_count > 0,
                "expense_id": expense_id,
                "deleted_count": result.deleted_count,
                "provider": "mongodb_atlas",
            }

        except PyMongoError as e:
            return {
                "success": False,
                "error": str(e),
                "expense_id": expense_id,
                "provider": "mongodb_atlas",
            }

    def search_expenses(
        self, query: Dict[str, Any], limit: int = 100
    ) -> List[Dict[str, Any]]:
        try:
            cursor = self.collection.find(query).limit(limit)
            results = list(cursor)

            for result in results:
                result["_id"] = str(result["_id"])

            return results

        except PyMongoError as e:
            raise Exception(f"MongoDB error: {str(e)}")

    def get_expenses_by_vendor(
        self, vendor_name: str, limit: int = 50
    ) -> List[Dict[str, Any]]:
        return self.search_expenses({"vendor": vendor_name}, limit)

    def get_expenses_by_date_range(
        self, start_date: str, end_date: str
    ) -> List[Dict[str, Any]]:
        query = {"date": {"$gte": start_date, "$lte": end_date}}
        return self.search_expenses(query)

    def get_expense_summary(self) -> Dict[str, Any]:
        try:
            pipeline = [
                {
                    "$group": {
                        "_id": None,
                        "total_expenses": {"$sum": 1},
                        "total_amount": {"$sum": "$total_amount"},
                        "average_amount": {"$avg": "$total_amount"},
                        "min_date": {"$min": "$date"},
                        "max_date": {"$max": "$date"},
                    }
                }
            ]

            result = list(self.collection.aggregate(pipeline))

            if result:
                summary = result[0]
                summary.pop("_id", None)
                summary["provider"] = "mongodb_atlas"
                return summary
            else:
                return {
                    "total_expenses": 0,
                    "total_amount": 0,
                    "average_amount": 0,
                    "provider": "mongodb_atlas",
                }

        except PyMongoError as e:
            raise Exception(f"MongoDB error: {str(e)}")

    def get_vendor_summary(self) -> List[Dict[str, Any]]:
        try:
            pipeline = [
                {
                    "$group": {
                        "_id": "$vendor",
                        "count": {"$sum": 1},
                        "total_amount": {"$sum": "$total_amount"},
                        "average_amount": {"$avg": "$total_amount"},
                    }
                },
                {"$sort": {"total_amount": -1}},
                {"$limit": 20},
            ]

            results = list(self.collection.aggregate(pipeline))

            for result in results:
                result["vendor"] = result.pop("_id")
                result["provider"] = "mongodb_atlas"

            return results

        except PyMongoError as e:
            raise Exception(f"MongoDB error: {str(e)}")

    def close(self):
        self.client.close()


def store_normalized_expense(normalized_expense: Dict[str, Any]) -> Dict[str, Any]:
    store = ExpenseRecordStore()

    try:
        result = store.store_expense_record(normalized_expense)
        return result
    finally:
        store.close()


def batch_store_normalized_expenses(
    normalized_expenses: List[Dict[str, Any]],
) -> Dict[str, Any]:
    store = ExpenseRecordStore()

    try:
        result = store.batch_store_expense_records(normalized_expenses)
        return result
    finally:
        store.close()


def query_expenses_by_criteria(criteria: Dict[str, Any]) -> List[Dict[str, Any]]:
    store = ExpenseRecordStore()

    try:
        results = store.search_expenses(criteria)
        return results
    finally:
        store.close()


def get_expense_analytics() -> Dict[str, Any]:
    store = ExpenseRecordStore()

    try:
        overall_summary = store.get_expense_summary()
        vendor_summary = store.get_vendor_summary()

        analytics = {
            "overall_summary": overall_summary,
            "vendor_summary": vendor_summary,
            "generated_at": datetime.utcnow().isoformat() + "Z",
            "data_source": "mongodb_atlas",
        }

        return analytics
    finally:
        store.close()
