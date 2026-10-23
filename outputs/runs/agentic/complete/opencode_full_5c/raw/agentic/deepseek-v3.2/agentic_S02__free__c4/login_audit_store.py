import os
from datetime import datetime
from typing import Dict, Any, List, Optional
from pymongo import MongoClient
from pymongo.errors import PyMongoError
import json


class LoginAuditStore:
    def __init__(self):
        mongodb_uri = os.environ.get("MONGODB_URI", "mongodb+srv://localhost:27017/")
        database_name = os.environ.get("MONGODB_DATABASE", "auth_audit")
        collection_name = os.environ.get("MONGODB_COLLECTION", "login_audits")

        self.client = MongoClient(mongodb_uri)
        self.db = self.client[database_name]
        self.collection = self.db[collection_name]

        self._ensure_indexes()

    def _ensure_indexes(self):
        try:
            self.collection.create_index([("timestamp", -1)])
            self.collection.create_index([("user_id", 1)])
            self.collection.create_index([("provider", 1)])
            self.collection.create_index([("success", 1)])
            self.collection.create_index([("timestamp", -1), ("provider", 1)])
        except PyMongoError as e:
            print(f"Warning: Could not create indexes: {e}")

    def store_login_audit(self, audit_data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            audit_record = {
                "user_id": audit_data.get("user_id", ""),
                "provider": audit_data.get("provider", ""),
                "timestamp": audit_data.get("timestamp", datetime.utcnow()),
                "ip_address": audit_data.get("ip_address"),
                "user_agent": audit_data.get("user_agent"),
                "success": audit_data.get("success", True),
                "error_message": audit_data.get("error_message"),
                "scopes_used": audit_data.get("scopes_used", []),
                "additional_data": audit_data.get("additional_data", {}),
                "created_at": datetime.utcnow(),
            }

            if isinstance(audit_record["timestamp"], str):
                audit_record["timestamp"] = datetime.fromisoformat(
                    audit_record["timestamp"]
                )

            result = self.collection.insert_one(audit_record)

            return {
                "success": True,
                "audit_id": str(result.inserted_id),
                "timestamp": audit_record["timestamp"].isoformat(),
            }
        except Exception as e:
            return {"success": False, "error": str(e), "audit_data": audit_data}

    def get_user_login_history(
        self, user_id: str, limit: int = 50
    ) -> List[Dict[str, Any]]:
        try:
            cursor = (
                self.collection.find({"user_id": user_id})
                .sort("timestamp", -1)
                .limit(limit)
            )

            history = []
            for doc in cursor:
                doc["_id"] = str(doc["_id"])
                if isinstance(doc.get("timestamp"), datetime):
                    doc["timestamp"] = doc["timestamp"].isoformat()
                if isinstance(doc.get("created_at"), datetime):
                    doc["created_at"] = doc["created_at"].isoformat()
                history.append(doc)

            return history
        except Exception as e:
            return []

    def get_provider_stats(self, days: int = 30) -> Dict[str, Any]:
        try:
            cutoff_date = datetime.utcnow() - timedelta(days=days)

            pipeline = [
                {"$match": {"timestamp": {"$gte": cutoff_date}}},
                {
                    "$group": {
                        "_id": "$provider",
                        "total_logins": {"$sum": 1},
                        "successful_logins": {
                            "$sum": {"$cond": [{"$eq": ["$success", True]}, 1, 0]}
                        },
                        "failed_logins": {
                            "$sum": {"$cond": [{"$eq": ["$success", False]}, 1, 0]}
                        },
                        "unique_users": {"$addToSet": "$user_id"},
                    }
                },
                {
                    "$project": {
                        "provider": "$_id",
                        "total_logins": 1,
                        "successful_logins": 1,
                        "failed_logins": 1,
                        "unique_user_count": {"$size": "$unique_users"},
                        "success_rate": {
                            "$multiply": [
                                {"$divide": ["$successful_logins", "$total_logins"]},
                                100,
                            ]
                        },
                    }
                },
                {"$sort": {"total_logins": -1}},
            ]

            results = list(self.collection.aggregate(pipeline))

            for result in results:
                result.pop("_id", None)

            return {
                "period_days": days,
                "cutoff_date": cutoff_date.isoformat(),
                "provider_stats": results,
                "total_providers": len(results),
            }
        except Exception as e:
            return {"error": str(e), "provider_stats": [], "total_providers": 0}

    def search_audits(
        self, filters: Dict[str, Any], limit: int = 100
    ) -> List[Dict[str, Any]]:
        try:
            query = {}

            if "user_id" in filters:
                query["user_id"] = filters["user_id"]

            if "provider" in filters:
                query["provider"] = filters["provider"]

            if "success" in filters:
                query["success"] = filters["success"]

            if "start_date" in filters and "end_date" in filters:
                start_date = datetime.fromisoformat(filters["start_date"])
                end_date = datetime.fromisoformat(filters["end_date"])
                query["timestamp"] = {"$gte": start_date, "$lte": end_date}

            cursor = self.collection.find(query).sort("timestamp", -1).limit(limit)

            results = []
            for doc in cursor:
                doc["_id"] = str(doc["_id"])
                if isinstance(doc.get("timestamp"), datetime):
                    doc["timestamp"] = doc["timestamp"].isoformat()
                if isinstance(doc.get("created_at"), datetime):
                    doc["created_at"] = doc["created_at"].isoformat()
                results.append(doc)

            return results
        except Exception as e:
            return []

    def delete_old_audits(self, days_to_keep: int = 365) -> Dict[str, Any]:
        try:
            cutoff_date = datetime.utcnow() - timedelta(days=days_to_keep)

            result = self.collection.delete_many({"timestamp": {"$lt": cutoff_date}})

            return {
                "success": True,
                "deleted_count": result.deleted_count,
                "cutoff_date": cutoff_date.isoformat(),
                "days_kept": days_to_keep,
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "cutoff_date": cutoff_date.isoformat()
                if "cutoff_date" in locals()
                else None,
            }

    def batch_store_audits(self, audits: List[Dict[str, Any]]) -> Dict[str, Any]:
        try:
            audit_records = []

            for audit in audits:
                record = {
                    "user_id": audit.get("user_id", ""),
                    "provider": audit.get("provider", ""),
                    "timestamp": audit.get("timestamp", datetime.utcnow()),
                    "ip_address": audit.get("ip_address"),
                    "user_agent": audit.get("user_agent"),
                    "success": audit.get("success", True),
                    "error_message": audit.get("error_message"),
                    "scopes_used": audit.get("scopes_used", []),
                    "additional_data": audit.get("additional_data", {}),
                    "created_at": datetime.utcnow(),
                }

                if isinstance(record["timestamp"], str):
                    record["timestamp"] = datetime.fromisoformat(record["timestamp"])

                audit_records.append(record)

            if audit_records:
                result = self.collection.insert_many(audit_records)

                return {
                    "success": True,
                    "inserted_count": len(result.inserted_ids),
                    "audit_ids": [str(id) for id in result.inserted_ids],
                }
            else:
                return {
                    "success": True,
                    "inserted_count": 0,
                    "message": "No audit records to insert",
                }
        except Exception as e:
            return {"success": False, "error": str(e), "audits_count": len(audits)}

    def close(self):
        self.client.close()


from datetime import timedelta
