import os
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import boto3
from botocore.exceptions import ClientError
from google.cloud import kms_v1
from google.api_core.exceptions import GoogleAPIError


def summarize_key_usage(key_id: str, days: int = 30) -> Dict[str, Any]:
    """
    Summarize key usage and crypto events from AWS CloudTrail and KMS.

    Args:
        key_id: AWS KMS key ID or alias
        days: Number of days to analyze

    Returns:
        Dictionary with key usage summary
    """
    # Initialize AWS clients
    kms_client = boto3.client(
        "kms", region_name=os.environ.get("AWS_REGION", "us-east-1")
    )

    cloudtrail_client = boto3.client(
        "cloudtrail", region_name=os.environ.get("AWS_REGION", "us-east-1")
    )

    try:
        # Get key metadata
        key_metadata = kms_client.describe_key(KeyId=key_id)["KeyMetadata"]

        # Calculate date range
        end_time = datetime.utcnow()
        start_time = end_time - timedelta(days=days)

        # Lookup events from CloudTrail
        events_response = cloudtrail_client.lookup_events(
            LookupAttributes=[
                {"AttributeKey": "ResourceName", "AttributeValue": key_metadata["Arn"]}
            ],
            StartTime=start_time,
            EndTime=end_time,
            MaxResults=100,
        )

        # Categorize events
        events = events_response.get("Events", [])
        event_counts = {}
        event_details = []

        for event in events:
            event_name = event.get("EventName", "Unknown")
            event_counts[event_name] = event_counts.get(event_name, 0) + 1

            event_details.append(
                {
                    "event_name": event_name,
                    "event_time": event.get("EventTime", "").isoformat()
                    if hasattr(event.get("EventTime"), "isoformat")
                    else str(event.get("EventTime", "")),
                    "username": event.get("Username", ""),
                    "source_ip": event.get("SourceIPAddress", ""),
                    "user_agent": event.get("UserAgent", ""),
                }
            )

        # Get KMS key usage metrics
        try:
            # Use CloudWatch metrics for KMS
            cloudwatch_client = boto3.client(
                "cloudwatch", region_name=os.environ.get("AWS_REGION", "us-east-1")
            )

            metrics_response = cloudwatch_client.get_metric_statistics(
                Namespace="AWS/KMS",
                MetricName="KeyUsage",
                Dimensions=[{"Name": "KeyId", "Value": key_metadata["KeyId"]}],
                StartTime=start_time,
                EndTime=end_time,
                Period=86400,  # 1 day in seconds
                Statistics=["Sum", "Average", "Maximum"],
            )

            datapoints = metrics_response.get("Datapoints", [])
            total_usage = sum(dp.get("Sum", 0) for dp in datapoints)
            avg_usage = (
                sum(dp.get("Average", 0) for dp in datapoints) / len(datapoints)
                if datapoints
                else 0
            )
            max_usage = max((dp.get("Maximum", 0) for dp in datapoints), default=0)
        except ClientError:
            # CloudWatch metrics might not be available
            total_usage = avg_usage = max_usage = 0

        # Prepare summary
        summary = {
            "key_id": key_metadata["KeyId"],
            "key_arn": key_metadata["Arn"],
            "key_state": key_metadata["KeyState"],
            "key_usage": key_metadata["KeyUsage"],
            "creation_date": key_metadata["CreationDate"].isoformat(),
            "enabled": key_metadata["Enabled"],
            "analysis_period_days": days,
            "analysis_start": start_time.isoformat(),
            "analysis_end": end_time.isoformat(),
            "total_events": len(events),
            "event_counts": event_counts,
            "event_details": event_details[:10],  # Limit details
            "usage_metrics": {
                "total_operations": total_usage,
                "average_daily_operations": avg_usage,
                "peak_daily_operations": max_usage,
            },
            "security_assessment": {
                "key_rotation_recommended": key_metadata["KeyState"] == "Enabled"
                and days > 90,
                "excessive_usage": total_usage > 10000,
                "unusual_activity": len(
                    [
                        e
                        for e in event_details
                        if e["event_name"] in ["Decrypt", "GenerateDataKey"]
                    ]
                )
                > 100,
                "multi_region_usage": False,  # Would need additional checks
            },
            "provider": "aws_kms",
            "generated_at": datetime.utcnow().isoformat(),
        }

        return summary

    except ClientError as e:
        raise Exception(f"AWS KMS/CloudTrail summary failed: {str(e)}")
    except Exception as e:
        raise Exception(f"Key usage summary failed: {str(e)}")


def compare_key_usage(key_ids: List[str], days: int = 30) -> Dict[str, Any]:
    """
    Compare usage across multiple keys.

    Args:
        key_ids: List of AWS KMS key IDs or aliases
        days: Number of days to analyze

    Returns:
        Dictionary with comparison data
    """
    comparisons = {}

    for key_id in key_ids:
        try:
            summary = summarize_key_usage(key_id, days)
            comparisons[key_id] = summary
        except Exception as e:
            comparisons[key_id] = {"error": str(e)}

    # Calculate statistics
    total_operations = 0
    enabled_keys = 0
    active_keys = 0

    for key_id, data in comparisons.items():
        if "error" not in data:
            total_operations += data["usage_metrics"]["total_operations"]
            if data["enabled"]:
                enabled_keys += 1
            if data["usage_metrics"]["total_operations"] > 0:
                active_keys += 1

    comparison_summary = {
        "keys_analyzed": len(key_ids),
        "enabled_keys": enabled_keys,
        "active_keys": active_keys,
        "total_operations_across_keys": total_operations,
        "average_operations_per_key": total_operations / len(comparisons)
        if comparisons
        else 0,
        "key_comparisons": comparisons,
        "provider": "aws_kms",
        "generated_at": datetime.utcnow().isoformat(),
    }

    return comparison_summary


def generate_crypto_audit_report(key_id: str) -> Dict[str, Any]:
    """
    Generate a comprehensive crypto audit report.

    Args:
        key_id: AWS KMS key ID or alias

    Returns:
        Dictionary with audit report
    """
    # Get usage summary
    usage_summary = summarize_key_usage(key_id, days=90)

    # Initialize AWS KMS client
    kms_client = boto3.client(
        "kms", region_name=os.environ.get("AWS_REGION", "us-east-1")
    )

    try:
        # Get key policy
        key_policy_response = kms_client.get_key_policy(
            KeyId=key_id, PolicyName="default"
        )

        key_policy = json.loads(key_policy_response["Policy"])

        # Get key rotation status
        rotation_response = kms_client.get_key_rotation_status(KeyId=key_id)

        # Check for grants
        grants_response = kms_client.list_grants(KeyId=key_id)

        # Prepare audit report
        audit_report = {
            "key_metadata": {
                "id": usage_summary["key_id"],
                "arn": usage_summary["key_arn"],
                "state": usage_summary["key_state"],
                "usage": usage_summary["key_usage"],
                "created": usage_summary["creation_date"],
                "enabled": usage_summary["enabled"],
            },
            "usage_analysis": usage_summary["usage_metrics"],
            "event_analysis": {
                "total_events": usage_summary["total_events"],
                "event_breakdown": usage_summary["event_counts"],
                "recent_events": usage_summary["event_details"],
            },
            "security_configuration": {
                "key_rotation_enabled": rotation_response["KeyRotationEnabled"],
                "automatic_rotation": rotation_response.get("RotationPeriodInDays", 0)
                > 0,
                "policy_exists": bool(key_policy),
                "policy_statement_count": len(key_policy.get("Statement", [])),
                "active_grants": len(grants_response.get("Grants", [])),
                "cross_account_access": any(
                    "AWS" in stmt.get("Principal", {})
                    for stmt in key_policy.get("Statement", [])
                ),
            },
            "compliance_checks": {
                "nist_800_57": {
                    "key_strength_adequate": usage_summary["key_usage"]
                    in ["ENCRYPT_DECRYPT", "SIGN_VERIFY"],
                    "key_rotation_compliant": rotation_response["KeyRotationEnabled"],
                    "access_controls_present": len(key_policy.get("Statement", [])) > 0,
                },
                "pci_dss": {
                    "key_management_procedures": usage_summary["key_state"]
                    == "Enabled",
                    "usage_logging_enabled": usage_summary["total_events"] > 0,
                },
                "hipaa": {
                    "encryption_standards_met": usage_summary["key_usage"]
                    in ["ENCRYPT_DECRYPT"],
                    "access_auditing_enabled": usage_summary["total_events"] > 0,
                },
            },
            "recommendations": [],
            "provider": "aws_kms",
            "audit_timestamp": datetime.utcnow().isoformat(),
        }

        # Generate recommendations
        if not rotation_response["KeyRotationEnabled"]:
            audit_report["recommendations"].append(
                "Enable automatic key rotation for compliance"
            )

        if usage_summary["total_events"] == 0:
            audit_report["recommendations"].append(
                "Enable CloudTrail logging for key usage monitoring"
            )

        if len(grants_response.get("Grants", [])) > 10:
            audit_report["recommendations"].append(
                "Review and clean up excessive key grants"
            )

        if usage_summary["security_assessment"]["excessive_usage"]:
            audit_report["recommendations"].append(
                "Investigate high key usage patterns"
            )

        return audit_report

    except ClientError as e:
        raise Exception(f"AWS KMS audit report failed: {str(e)}")
    except Exception as e:
        raise Exception(f"Crypto audit report failed: {str(e)}")
