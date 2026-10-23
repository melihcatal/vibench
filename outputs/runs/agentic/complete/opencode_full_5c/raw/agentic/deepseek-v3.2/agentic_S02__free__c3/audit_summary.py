import os
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any
import boto3
from botocore.exceptions import ClientError


class AuditSummary:
    def __init__(self):
        self.dynamodb = boto3.resource(
            "dynamodb",
            region_name=os.environ.get("AWS_REGION", "us-east-1"),
            aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        )
        self.table_name = os.environ.get("AUDIT_TABLE_NAME", "federated-login-audit")
        self.table = self.dynamodb.Table(self.table_name)

    def summarize_daily_logins(self, date: str = None) -> Dict[str, Any]:
        if not date:
            date = datetime.now().strftime("%Y-%m-%d")

        try:
            response = self.table.query(
                IndexName="date-index",
                KeyConditionExpression="#d = :date",
                ExpressionAttributeNames={"#d": "date"},
                ExpressionAttributeValues={":date": date},
            )

            items = response.get("Items", [])

            summary = {
                "date": date,
                "total_logins": len(items),
                "providers": {},
                "success_rate": 0,
                "hourly_breakdown": {},
                "unique_users": set(),
            }

            successful_logins = 0

            for item in items:
                provider = item.get("provider", "unknown")
                summary["providers"][provider] = (
                    summary["providers"].get(provider, 0) + 1
                )

                if item.get("status") == "success":
                    successful_logins += 1

                user_id = item.get("user_id")
                if user_id:
                    summary["unique_users"].add(user_id)

                timestamp = item.get("timestamp")
                if timestamp:
                    try:
                        hour = datetime.fromisoformat(timestamp).hour
                        summary["hourly_breakdown"][hour] = (
                            summary["hourly_breakdown"].get(hour, 0) + 1
                        )
                    except (ValueError, TypeError):
                        pass

            if summary["total_logins"] > 0:
                summary["success_rate"] = (
                    successful_logins / summary["total_logins"]
                ) * 100

            summary["unique_users_count"] = len(summary["unique_users"])
            summary.pop("unique_users", None)

            summary["hourly_breakdown"] = dict(
                sorted(summary["hourly_breakdown"].items())
            )

            return summary

        except ClientError as e:
            return {"error": f"DynamoDB query failed: {str(e)}"}

    def summarize_provider_performance(self, days: int = 7) -> Dict[str, Any]:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)

        summaries = []

        for i in range(days):
            current_date = start_date + timedelta(days=i)
            date_str = current_date.strftime("%Y-%m-%d")

            try:
                response = self.table.query(
                    IndexName="date-index",
                    KeyConditionExpression="#d = :date",
                    ExpressionAttributeNames={"#d": "date"},
                    ExpressionAttributeValues={":date": date_str},
                )

                items = response.get("Items", [])

                provider_stats = {}
                for item in items:
                    provider = item.get("provider", "unknown")
                    if provider not in provider_stats:
                        provider_stats[provider] = {"total": 0, "success": 0}

                    provider_stats[provider]["total"] += 1
                    if item.get("status") == "success":
                        provider_stats[provider]["success"] += 1

                for provider, stats in provider_stats.items():
                    if stats["total"] > 0:
                        stats["success_rate"] = (
                            stats["success"] / stats["total"]
                        ) * 100
                    else:
                        stats["success_rate"] = 0

                summaries.append({"date": date_str, "providers": provider_stats})

            except ClientError:
                continue

        overall_stats = {}
        for summary in summaries:
            for provider, stats in summary["providers"].items():
                if provider not in overall_stats:
                    overall_stats[provider] = {"total": 0, "success": 0}

                overall_stats[provider]["total"] += stats["total"]
                overall_stats[provider]["success"] += stats["success"]

        for provider, stats in overall_stats.items():
            if stats["total"] > 0:
                stats["success_rate"] = (stats["success"] / stats["total"]) * 100
            else:
                stats["success_rate"] = 0

        return {
            "period": f"{days} days",
            "start_date": start_date.strftime("%Y-%m-%d"),
            "end_date": end_date.strftime("%Y-%m-%d"),
            "daily_summaries": summaries,
            "overall_provider_stats": overall_stats,
        }

    def get_recent_failed_logins(self, limit: int = 50) -> List[Dict[str, Any]]:
        try:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=1)

            response = self.table.scan(
                FilterExpression="#s = :status AND #t BETWEEN :start AND :end",
                ExpressionAttributeNames={"#s": "status", "#t": "timestamp"},
                ExpressionAttributeValues={
                    ":status": "failed",
                    ":start": start_date.isoformat(),
                    ":end": end_date.isoformat(),
                },
                Limit=limit,
            )

            failed_logins = response.get("Items", [])

            for login in failed_logins:
                if "error_details" in login:
                    try:
                        login["error_details"] = json.loads(login["error_details"])
                    except (json.JSONDecodeError, TypeError):
                        pass

            return failed_logins

        except ClientError as e:
            return [{"error": f"DynamoDB scan failed: {str(e)}"}]
