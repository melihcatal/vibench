import os
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import boto3
from botocore.exceptions import ClientError
from security_models import CryptoEvent, normalize_timestamp


class KeyUsageSummary:
    """Summarize key usage and crypto events using AWS CloudWatch."""

    def __init__(self, region: Optional[str] = None):
        self.region = region or os.getenv("AWS_REGION", "us-east-1")
        self.cloudwatch = boto3.client("cloudwatch", region_name=self.region)
        self.kms = boto3.client("kms", region_name=self.region)

    def get_key_usage_metrics(self, key_id: str, days: int = 7) -> Dict[str, Any]:
        """
        Get CloudWatch metrics for KMS key usage.

        Args:
            key_id: AWS KMS key ID or alias
            days: Number of days to look back

        Returns:
            Dictionary with key usage metrics
        """
        end_time = datetime.utcnow()
        start_time = end_time - timedelta(days=days)

        try:
            # Get key description first
            key_info = self.kms.describe_key(KeyId=key_id)
            key_arn = key_info["KeyMetadata"]["Arn"]

            # Query CloudWatch metrics for KMS operations
            response = self.cloudwatch.get_metric_data(
                MetricDataQueries=[
                    {
                        "Id": "encrypt",
                        "MetricStat": {
                            "Metric": {
                                "Namespace": "AWS/KMS",
                                "MetricName": "Encrypt",
                                "Dimensions": [{"Name": "KeyId", "Value": key_id}],
                            },
                            "Period": 86400,  # 1 day in seconds
                            "Stat": "Sum",
                        },
                        "ReturnData": True,
                    },
                    {
                        "Id": "decrypt",
                        "MetricStat": {
                            "Metric": {
                                "Namespace": "AWS/KMS",
                                "MetricName": "Decrypt",
                                "Dimensions": [{"Name": "KeyId", "Value": key_id}],
                            },
                            "Period": 86400,
                            "Stat": "Sum",
                        },
                        "ReturnData": True,
                    },
                    {
                        "Id": "generate_data_key",
                        "MetricStat": {
                            "Metric": {
                                "Namespace": "AWS/KMS",
                                "MetricName": "GenerateDataKey",
                                "Dimensions": [{"Name": "KeyId", "Value": key_id}],
                            },
                            "Period": 86400,
                            "Stat": "Sum",
                        },
                        "ReturnData": True,
                    },
                    {
                        "Id": "sign",
                        "MetricStat": {
                            "Metric": {
                                "Namespace": "AWS/KMS",
                                "MetricName": "Sign",
                                "Dimensions": [{"Name": "KeyId", "Value": key_id}],
                            },
                            "Period": 86400,
                            "Stat": "Sum",
                        },
                        "ReturnData": True,
                    },
                ],
                StartTime=start_time,
                EndTime=end_time,
            )

            # Process metrics
            metrics_summary = {
                "key_id": key_id,
                "key_arn": key_arn,
                "period_days": days,
                "provider": "aws_cloudwatch",
                "metrics": {},
            }

            for result in response["MetricDataResults"]:
                metric_name = result["Label"]
                values = result["Values"]
                timestamps = result["Timestamps"]

                if values:
                    metrics_summary["metrics"][metric_name] = {
                        "total": sum(values),
                        "daily_average": sum(values) / len(values),
                        "max_daily": max(values),
                        "min_daily": min(values),
                        "timestamps": [ts.isoformat() for ts in timestamps],
                        "values": values,
                    }
                else:
                    metrics_summary["metrics"][metric_name] = {
                        "total": 0,
                        "daily_average": 0,
                        "max_daily": 0,
                        "min_daily": 0,
                        "timestamps": [],
                        "values": [],
                    }

            return metrics_summary

        except ClientError as e:
            raise Exception(f"Failed to get key usage metrics: {e}")

    def summarize_crypto_events(self, events: List[CryptoEvent]) -> Dict[str, Any]:
        """
        Summarize a list of crypto events.

        Args:
            events: List of CryptoEvent objects

        Returns:
            Summary statistics
        """
        if not events:
            return {"total_events": 0, "summary": {}, "provider": "local_analysis"}

        summary = {
            "total_events": len(events),
            "successful_events": sum(1 for e in events if e.success),
            "failed_events": sum(1 for e in events if not e.success),
            "operations": {},
            "keys_used": set(),
            "algorithms_used": set(),
            "provider": "local_analysis",
        }

        # Group by operation type
        for event in events:
            op = event.operation
            if op not in summary["operations"]:
                summary["operations"][op] = {"count": 0, "success": 0, "fail": 0}

            summary["operations"][op]["count"] += 1
            if event.success:
                summary["operations"][op]["success"] += 1
            else:
                summary["operations"][op]["fail"] += 1

            summary["keys_used"].add(event.key_id)
            summary["algorithms_used"].add(event.algorithm)

        # Convert sets to lists for JSON serialization
        summary["keys_used"] = list(summary["keys_used"])
        summary["algorithms_used"] = list(summary["algorithms_used"])

        # Calculate success rates
        for op in summary["operations"]:
            op_data = summary["operations"][op]
            if op_data["count"] > 0:
                op_data["success_rate"] = (op_data["success"] / op_data["count"]) * 100
            else:
                op_data["success_rate"] = 0

        return summary

    def generate_usage_report(
        self, key_ids: List[str], days: int = 30
    ) -> Dict[str, Any]:
        """
        Generate comprehensive usage report for multiple keys.

        Args:
            key_ids: List of key IDs to analyze
            days: Number of days to analyze

        Returns:
            Comprehensive usage report
        """
        report = {
            "generated_at": normalize_timestamp(),
            "period_days": days,
            "keys_analyzed": len(key_ids),
            "provider": "aws_cloudwatch",
            "key_reports": [],
            "overall_summary": {
                "total_encrypt_operations": 0,
                "total_decrypt_operations": 0,
                "total_generate_data_key_operations": 0,
                "total_sign_operations": 0,
                "most_active_key": None,
                "most_active_operation": None,
            },
        }

        max_operations = 0
        operation_counts = {}

        for key_id in key_ids:
            try:
                key_metrics = self.get_key_usage_metrics(key_id, days)
                report["key_reports"].append(key_metrics)

                # Update overall summary
                for metric_name, metric_data in key_metrics["metrics"].items():
                    total = metric_data["total"]

                    if metric_name not in operation_counts:
                        operation_counts[metric_name] = 0
                    operation_counts[metric_name] += total

                    # Update report field based on metric name
                    if metric_name == "Encrypt":
                        report["overall_summary"]["total_encrypt_operations"] += total
                    elif metric_name == "Decrypt":
                        report["overall_summary"]["total_decrypt_operations"] += total
                    elif metric_name == "GenerateDataKey":
                        report["overall_summary"][
                            "total_generate_data_key_operations"
                        ] += total
                    elif metric_name == "Sign":
                        report["overall_summary"]["total_sign_operations"] += total

                    # Track most active key
                    if total > max_operations:
                        max_operations = total
                        report["overall_summary"]["most_active_key"] = key_id

            except Exception as e:
                report["key_reports"].append(
                    {"key_id": key_id, "error": str(e), "provider": "aws_cloudwatch"}
                )

        # Determine most active operation
        if operation_counts:
            report["overall_summary"]["most_active_operation"] = max(
                operation_counts, key=operation_counts.get
            )

        return report


if __name__ == "__main__":
    # Example usage
    summarizer = KeyUsageSummary()

    # Get metrics for a specific key
    try:
        key_metrics = summarizer.get_key_usage_metrics("alias/encryption-key", days=7)
        print(f"Key metrics: {json.dumps(key_metrics, indent=2)}")
    except Exception as e:
        print(f"Error getting metrics: {e}")

    # Generate report for multiple keys
    report = summarizer.generate_usage_report(
        ["alias/encryption-key", "alias/signing-key"], days=30
    )
    print(f"\nUsage report: {json.dumps(report, indent=2)}")
