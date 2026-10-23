import os
from datetime import datetime, timedelta
from typing import Dict, List, Any
import boto3
from boto3.dynamodb.conditions import Key
import json


def summarize_login_audits(days: int = 7, region: str = "us-east-1") -> Dict[str, Any]:
    dynamodb = boto3.resource(
        "dynamodb",
        region_name=region,
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
    )

    table_name = os.environ.get("DYNAMODB_AUDIT_TABLE", "federated-login-audits")
    table = dynamodb.Table(table_name)

    end_time = datetime.utcnow()
    start_time = end_time - timedelta(days=days)

    try:
        response = table.scan(
            FilterExpression=Key("timestamp").between(
                start_time.isoformat(), end_time.isoformat()
            )
        )

        items = response.get("Items", [])

        while "LastEvaluatedKey" in response:
            response = table.scan(
                ExclusiveStartKey=response["LastEvaluatedKey"],
                FilterExpression=Key("timestamp").between(
                    start_time.isoformat(), end_time.isoformat()
                ),
            )
            items.extend(response.get("Items", []))

        summary = {
            "total_logins": len(items),
            "successful_logins": 0,
            "failed_logins": 0,
            "providers": {},
            "daily_breakdown": {},
            "top_users": {},
            "error_summary": {},
        }

        for item in items:
            provider = item.get("provider", "unknown")
            success = item.get("success", True)
            user_id = item.get("user_id", "unknown")
            timestamp = item.get("timestamp", "")
            error_message = item.get("error_message")

            if success:
                summary["successful_logins"] += 1
            else:
                summary["failed_logins"] += 1

            if provider not in summary["providers"]:
                summary["providers"][provider] = {
                    "total": 0,
                    "successful": 0,
                    "failed": 0,
                }

            summary["providers"][provider]["total"] += 1
            if success:
                summary["providers"][provider]["successful"] += 1
            else:
                summary["providers"][provider]["failed"] += 1

            if user_id not in summary["top_users"]:
                summary["top_users"][user_id] = 0
            summary["top_users"][user_id] += 1

            if timestamp:
                try:
                    login_date = datetime.fromisoformat(timestamp).date().isoformat()
                    if login_date not in summary["daily_breakdown"]:
                        summary["daily_breakdown"][login_date] = 0
                    summary["daily_breakdown"][login_date] += 1
                except:
                    pass

            if error_message and not success:
                if error_message not in summary["error_summary"]:
                    summary["error_summary"][error_message] = 0
                summary["error_summary"][error_message] += 1

        summary["success_rate"] = (
            (summary["successful_logins"] / summary["total_logins"] * 100)
            if summary["total_logins"] > 0
            else 0
        )

        summary["top_users"] = dict(
            sorted(summary["top_users"].items(), key=lambda x: x[1], reverse=True)[:10]
        )

        summary["daily_breakdown"] = dict(sorted(summary["daily_breakdown"].items()))

        summary["error_summary"] = dict(
            sorted(summary["error_summary"].items(), key=lambda x: x[1], reverse=True)[
                :5
            ]
        )

        return summary

    except Exception as e:
        return {
            "error": str(e),
            "total_logins": 0,
            "successful_logins": 0,
            "failed_logins": 0,
            "providers": {},
            "daily_breakdown": {},
            "top_users": {},
            "error_summary": {},
        }


def generate_audit_report(days: int = 30) -> Dict[str, Any]:
    summary = summarize_login_audits(days)

    report = {
        "report_generated": datetime.utcnow().isoformat(),
        "period_days": days,
        "summary": summary,
        "insights": [],
    }

    if summary.get("total_logins", 0) > 0:
        if summary["success_rate"] < 95:
            report["insights"].append(
                {
                    "type": "warning",
                    "message": f"Login success rate is {summary['success_rate']:.1f}%, below 95% threshold",
                }
            )

        most_used_provider = (
            max(summary["providers"].items(), key=lambda x: x[1]["total"])
            if summary["providers"]
            else ("none", {"total": 0})
        )

        report["insights"].append(
            {
                "type": "info",
                "message": f"Most used provider: {most_used_provider[0]} ({most_used_provider[1]['total']} logins)",
            }
        )

        if summary["failed_logins"] > 0 and summary["error_summary"]:
            top_error = list(summary["error_summary"].items())[0]
            report["insights"].append(
                {
                    "type": "error",
                    "message": f"Most common error: {top_error[0]} ({top_error[1]} occurrences)",
                }
            )

    return report
