import os
import json
from datetime import datetime
from typing import Dict, List, Any, Optional
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database
from bson import ObjectId
from document_models import NormalizedExpense


class ExpenseRecordStore:
    def __init__(self):
        self.connection_string = os.getenv("MONGODB_ATLAS_URI")
        if not self.connection_string:
            raise ValueError("MONGODB_ATLAS_URI environment variable is required")

        self.client = MongoClient(self.connection_string)
        self.db = self.client.get_database("expense_tracker")
        self.collection = self.db.get_collection("expense_records")

        self._ensure_indexes()

    def _ensure_indexes(self):
        self.collection.create_index([("expense_id", 1)], unique=True)
        self.collection.create_index([("vendor", 1)])
        self.collection.create_index([("date", -1)])
        self.collection.create_index([("total_amount", -1)])
        self.collection.create_index([("confidence_score", -1)])

    def save_expense(self, expense: NormalizedExpense) -> Dict[str, Any]:
        expense_dict = {
            "expense_id": expense.expense_id,
            "vendor": expense.vendor,
            "date": expense.date,
            "total_amount": expense.total_amount,
            "currency": expense.currency,
            "line_items": expense.line_items,
            "metadata": expense.metadata,
            "confidence_score": expense.confidence_score,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
            "status": "active",
        }

        result = self.collection.update_one(
            {"expense_id": expense.expense_id}, {"$set": expense_dict}, upsert=True
        )

        return {
            "expense_id": expense.expense_id,
            "upserted_id": str(result.upserted_id) if result.upserted_id else None,
            "matched_count": result.matched_count,
            "modified_count": result.modified_count,
            "operation": "insert" if result.upserted_id else "update",
        }

    def get_expense_by_id(self, expense_id: str) -> Optional[Dict[str, Any]]:
        document = self.collection.find_one({"expense_id": expense_id})
        if document:
            document["_id"] = str(document["_id"])
            return document
        return None

    def get_expenses_by_vendor(
        self, vendor: str, limit: int = 100
    ) -> List[Dict[str, Any]]:
        cursor = (
            self.collection.find({"vendor": {"$regex": vendor, "$options": "i"}})
            .sort("date", -1)
            .limit(limit)
        )

        expenses = []
        for doc in cursor:
            doc["_id"] = str(doc["_id"])
            expenses.append(doc)

        return expenses

    def get_expenses_by_date_range(
        self, start_date: datetime, end_date: datetime
    ) -> List[Dict[str, Any]]:
        cursor = self.collection.find(
            {"date": {"$gte": start_date, "$lte": end_date}}
        ).sort("date", -1)

        expenses = []
        for doc in cursor:
            doc["_id"] = str(doc["_id"])
            expenses.append(doc)

        return expenses

    def get_high_value_expenses(
        self, min_amount: float = 1000.0
    ) -> List[Dict[str, Any]]:
        cursor = self.collection.find({"total_amount": {"$gte": min_amount}}).sort(
            "total_amount", -1
        )

        expenses = []
        for doc in cursor:
            doc["_id"] = str(doc["_id"])
            expenses.append(doc)

        return expenses

    def get_low_confidence_expenses(
        self, max_confidence: float = 0.5
    ) -> List[Dict[str, Any]]:
        cursor = self.collection.find(
            {"confidence_score": {"$lte": max_confidence}}
        ).sort("confidence_score", 1)

        expenses = []
        for doc in cursor:
            doc["_id"] = str(doc["_id"])
            expenses.append(doc)

        return expenses

    def update_expense_status(self, expense_id: str, status: str) -> bool:
        result = self.collection.update_one(
            {"expense_id": expense_id},
            {"$set": {"status": status, "updated_at": datetime.utcnow()}},
        )

        return result.modified_count > 0

    def delete_expense(self, expense_id: str) -> bool:
        result = self.collection.delete_one({"expense_id": expense_id})
        return result.deleted_count > 0

    def get_expense_statistics(self) -> Dict[str, Any]:
        pipeline = [
            {
                "$group": {
                    "_id": None,
                    "total_expenses": {"$sum": 1},
                    "total_amount": {"$sum": "$total_amount"},
                    "avg_amount": {"$avg": "$total_amount"},
                    "max_amount": {"$max": "$total_amount"},
                    "min_amount": {"$min": "$total_amount"},
                    "avg_confidence": {"$avg": "$confidence_score"},
                }
            }
        ]

        result = list(self.collection.aggregate(pipeline))
        if result:
            stats = result[0]
            stats.pop("_id", None)
            return stats

        return {
            "total_expenses": 0,
            "total_amount": 0,
            "avg_amount": 0,
            "max_amount": 0,
            "min_amount": 0,
            "avg_confidence": 0,
        }

    def get_vendor_statistics(self) -> List[Dict[str, Any]]:
        pipeline = [
            {
                "$group": {
                    "_id": "$vendor",
                    "count": {"$sum": 1},
                    "total_amount": {"$sum": "$total_amount"},
                    "avg_amount": {"$avg": "$total_amount"},
                }
            },
            {"$sort": {"total_amount": -1}},
            {"$limit": 20},
        ]

        results = list(self.collection.aggregate(pipeline))

        vendor_stats = []
        for res in results:
            vendor_stats.append(
                {
                    "vendor": res["_id"],
                    "expense_count": res["count"],
                    "total_amount": res["total_amount"],
                    "average_amount": res["avg_amount"],
                }
            )

        return vendor_stats

    def search_expenses(
        self, query: str, field: str = "vendor"
    ) -> List[Dict[str, Any]]:
        cursor = (
            self.collection.find({field: {"$regex": query, "$options": "i"}})
            .sort("date", -1)
            .limit(50)
        )

        expenses = []
        for doc in cursor:
            doc["_id"] = str(doc["_id"])
            expenses.append(doc)

        return expenses

    def close(self):
        self.client.close()


def save_expense_to_store(expense: NormalizedExpense) -> Dict[str, Any]:
    store = ExpenseRecordStore()
    try:
        result = store.save_expense(expense)
        return {
            "success": True,
            "expense_id": expense.expense_id,
            "result": result,
            "message": f"Expense {expense.expense_id} saved successfully",
        }
    except Exception as e:
        return {
            "success": False,
            "expense_id": expense.expense_id,
            "error": str(e),
            "message": f"Failed to save expense {expense.expense_id}",
        }
    finally:
        store.close()


def batch_save_expenses(expenses: List[NormalizedExpense]) -> Dict[str, Any]:
    store = ExpenseRecordStore()
    try:
        results = []
        success_count = 0
        failure_count = 0

        for expense in expenses:
            try:
                result = store.save_expense(expense)
                results.append(
                    {
                        "expense_id": expense.expense_id,
                        "success": True,
                        "result": result,
                    }
                )
                success_count += 1
            except Exception as e:
                results.append(
                    {
                        "expense_id": expense.expense_id,
                        "success": False,
                        "error": str(e),
                    }
                )
                failure_count += 1

        return {
            "total": len(expenses),
            "success": success_count,
            "failed": failure_count,
            "results": results,
        }
    finally:
        store.close()
