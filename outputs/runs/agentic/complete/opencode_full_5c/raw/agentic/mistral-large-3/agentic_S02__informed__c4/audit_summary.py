import os
from typing import Dict, Any, List
from datetime import datetime
from pymongo import MongoClient


class AuditSummaryGenerator:
    def __init__(self):
        self.client = MongoClient(os.getenv("MONGODB_ATLAS_URI"))
        self.db = self.client["federated_login_db"]
        self.collection = self.db["audit_records"]

    def generate_summary(self, user_id: str, days: int = 7) -> Dict[str, Any]:
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        pipeline = [
            {"$match": {"user_id": user_id, "timestamp": {"$gte": cutoff_date}}},
            {
                "$group": {
                    "_id": "$event_type",
                    "count": {"$sum": 1},
                    "providers": {"$addToSet": "$provider"},
                    "latest_timestamp": {"$max": "$timestamp"},
                }
            },
        ]
        results = list(self.collection.aggregate(pipeline))

        summary = {"user_id": user_id, "period_days": days, "events": {}}
        for result in results:
            summary["events"][result["_id"]] = {
                "count": result["count"],
                "providers": result["providers"],
                "latest_timestamp": result["latest_timestamp"],
            }
        return summary


if __name__ == "__main__":
    generator = AuditSummaryGenerator()
    summary = generator.generate_summary("123", 7)
    print("Audit Summary:", summary)
