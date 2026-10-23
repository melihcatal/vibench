import os
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import boto3
from botocore.exceptions import ClientError
from google.cloud import monitoring_v3
from google.cloud.monitoring_v3 import query
from azure.mgmt.keyvault import KeyVaultManagementClient
from azure.identity import DefaultAzureCredential


class KeyUsageSummary:
    """Summarize key usage and crypto events from managed key services."""

    def __init__(self):
        self.aws_region = os.environ.get("AWS_REGION", "us-east-1")
        self.gcp_project_id = os.environ.get("GCP_PROJECT_ID", "my-project")
        self.azure_subscription_id = os.environ.get("AZURE_SUBSCRIPTION_ID", "")

    def get_aws_kms_usage_summary(
        self, key_id: Optional[str] = None, days: int = 30
    ) -> Dict:
        """
        Get AWS KMS key usage summary.

        Args:
            key_id: Optional specific key ID
            days: Number of days to look back

        Returns:
            Dict with usage summary
        """
        kms_client = boto3.client("kms", region_name=self.aws_region)
        cloudwatch_client = boto3.client("cloudwatch", region_name=self.aws_region)

        try:
            # List keys if no specific key provided
            if key_id:
                keys = [{"KeyId": key_id}]
            else:
                keys_response = kms_client.list_keys(Limit=100)
                keys = keys_response["Keys"]

            summary = {
                "provider": "aws_kms",
                "total_keys": len(keys),
                "keys": [],
                "period_days": days,
                "generated_at": datetime.utcnow().isoformat() + "Z",
            }

            for key in keys:
                key_info = self._get_aws_key_info(
                    kms_client, cloudwatch_client, key["KeyId"], days
                )
                summary["keys"].append(key_info)

            # Calculate totals
            summary["total_encryptions"] = sum(
                k.get("encryption_count", 0) for k in summary["keys"]
            )
            summary["total_decryptions"] = sum(
                k.get("decryption_count", 0) for k in summary["keys"]
            )
            summary["total_generations"] = sum(
                k.get("generation_count", 0) for k in summary["keys"]
            )

            return summary

        except ClientError as e:
            raise Exception(f"AWS KMS usage summary error: {e}")

    def _get_aws_key_info(
        self, kms_client, cloudwatch_client, key_id: str, days: int
    ) -> Dict:
        """Get detailed info for a specific AWS KMS key."""
        try:
            # Get key metadata
            key_metadata = kms_client.describe_key(KeyId=key_id)["KeyMetadata"]

            # Get CloudWatch metrics for the key
            end_time = datetime.utcnow()
            start_time = end_time - timedelta(days=days)

            metrics = self._get_aws_key_metrics(
                cloudwatch_client, key_id, start_time, end_time
            )

            return {
                "key_id": key_id,
                "arn": key_metadata.get("Arn"),
                "key_state": key_metadata.get("KeyState"),
                "key_usage": key_metadata.get("KeyUsage"),
                "creation_date": key_metadata.get("CreationDate").isoformat()
                if key_metadata.get("CreationDate")
                else None,
                "description": key_metadata.get("Description"),
                "encryption_count": metrics.get("Encrypt", 0),
                "decryption_count": metrics.get("Decrypt", 0),
                "generation_count": metrics.get("GenerateDataKey", 0),
                "metrics_period_days": days,
            }

        except ClientError as e:
            return {
                "key_id": key_id,
                "error": str(e),
                "encryption_count": 0,
                "decryption_count": 0,
                "generation_count": 0,
            }

    def _get_aws_key_metrics(
        self, cloudwatch_client, key_id: str, start_time: datetime, end_time: datetime
    ) -> Dict:
        """Get CloudWatch metrics for AWS KMS key."""
        metrics = {}

        # Metric names for KMS
        metric_queries = [
            ("Encrypt", "CallCount", "Encrypt"),
            ("Decrypt", "CallCount", "Decrypt"),
            ("GenerateDataKey", "CallCount", "GenerateDataKey"),
        ]

        for metric_name, stat, operation in metric_queries:
            try:
                response = cloudwatch_client.get_metric_statistics(
                    Namespace="AWS/KMS",
                    MetricName=metric_name,
                    Dimensions=[{"Name": "KeyId", "Value": key_id}],
                    StartTime=start_time,
                    EndTime=end_time,
                    Period=86400,  # 1 day in seconds
                    Statistics=["Sum"],
                )

                if response["Datapoints"]:
                    total = sum(dp["Sum"] for dp in response["Datapoints"])
                    metrics[operation] = int(total)
                else:
                    metrics[operation] = 0

            except ClientError:
                metrics[operation] = 0

        return metrics

    def get_gcp_kms_usage_summary(
        self, key_name: Optional[str] = None, days: int = 30
    ) -> Dict:
        """
        Get GCP KMS key usage summary.

        Args:
            key_name: Optional specific key name
            days: Number of days to look back

        Returns:
            Dict with usage summary
        """
        try:
            # Initialize Cloud Monitoring client
            client = monitoring_v3.MetricServiceClient()

            # Build query for KMS metrics
            project_name = f"projects/{self.gcp_project_id}"

            # For simplicity, return a structured summary
            # In a real implementation, you would query Cloud Monitoring metrics
            summary = {
                "provider": "gcp_kms",
                "project_id": self.gcp_project_id,
                "period_days": days,
                "generated_at": datetime.utcnow().isoformat() + "Z",
                "note": "GCP KMS metrics require Cloud Monitoring setup. This is a placeholder implementation.",
            }

            if key_name:
                summary["key_name"] = key_name
                summary["key_info"] = {
                    "name": key_name,
                    "encryption_operations": "N/A - requires monitoring",
                    "decryption_operations": "N/A - requires monitoring",
                }

            return summary

        except Exception as e:
            raise Exception(f"GCP KMS usage summary error: {e}")

    def get_azure_keyvault_usage_summary(
        self, vault_name: Optional[str] = None, days: int = 30
    ) -> Dict:
        """
        Get Azure Key Vault usage summary.

        Args:
            vault_name: Optional specific vault name
            days: Number of days to look back

        Returns:
            Dict with usage summary
        """
        if not self.azure_subscription_id:
            raise ValueError("AZURE_SUBSCRIPTION_ID environment variable is required")

        try:
            credential = DefaultAzureCredential()
            kv_client = KeyVaultManagementClient(credential, self.azure_subscription_id)

            # List vaults if no specific vault provided
            if vault_name:
                vaults = [kv_client.vaults.get("resource-group", vault_name)]
            else:
                vaults = list(kv_client.vaults.list())

            summary = {
                "provider": "azure_keyvault",
                "total_vaults": len(vaults),
                "vaults": [],
                "period_days": days,
                "generated_at": datetime.utcnow().isoformat() + "Z",
                "note": "Detailed metrics require Azure Monitor setup. This shows vault information only.",
            }

            for vault in vaults:
                vault_info = {
                    "vault_name": vault.name,
                    "location": vault.location,
                    "sku": vault.properties.sku.name
                    if vault.properties.sku
                    else "Unknown",
                    "enabled_for_deployment": vault.properties.enabled_for_deployment,
                    "enabled_for_disk_encryption": vault.properties.enabled_for_disk_encryption,
                    "enabled_for_template_deployment": vault.properties.enabled_for_template_deployment,
                    "soft_delete_enabled": getattr(
                        vault.properties, "enable_soft_delete", False
                    ),
                    "purge_protection_enabled": getattr(
                        vault.properties, "enable_purge_protection", False
                    ),
                }
                summary["vaults"].append(vault_info)

            return summary

        except Exception as e:
            raise Exception(f"Azure Key Vault usage summary error: {e}")

    def generate_comprehensive_summary(self, provider: str = "aws", **kwargs) -> Dict:
        """
        Generate comprehensive key usage summary.

        Args:
            provider: 'aws', 'gcp', or 'azure'
            **kwargs: Provider-specific arguments

        Returns:
            Comprehensive summary dict
        """
        if provider.lower() == "aws":
            key_id = kwargs.get("key_id")
            days = kwargs.get("days", 30)
            return self.get_aws_kms_usage_summary(key_id, days)

        elif provider.lower() == "gcp":
            key_name = kwargs.get("key_name")
            days = kwargs.get("days", 30)
            return self.get_gcp_kms_usage_summary(key_name, days)

        elif provider.lower() == "azure":
            vault_name = kwargs.get("vault_name")
            days = kwargs.get("days", 30)
            return self.get_azure_keyvault_usage_summary(vault_name, days)

        else:
            raise ValueError(f"Unsupported provider: {provider}")

    def export_summary_to_json(
        self, summary: Dict, filepath: Optional[str] = None
    ) -> str:
        """
        Export summary to JSON format.

        Args:
            summary: Summary dict
            filepath: Optional file path to save

        Returns:
            JSON string
        """
        json_str = json.dumps(summary, indent=2, default=str)

        if filepath:
            with open(filepath, "w") as f:
                f.write(json_str)

        return json_str

    def get_key_health_status(self, provider: str, key_id: str) -> Dict:
        """
        Get health/status of a specific key.

        Args:
            provider: 'aws', 'gcp', or 'azure'
            key_id: Key identifier

        Returns:
            Health status dict
        """
        if provider.lower() == "aws":
            return self._get_aws_key_health(key_id)
        elif provider.lower() == "gcp":
            return self._get_gcp_key_health(key_id)
        elif provider.lower() == "azure":
            return self._get_azure_key_health(key_id)
        else:
            raise ValueError(f"Unsupported provider: {provider}")

    def _get_aws_key_health(self, key_id: str) -> Dict:
        """Get AWS KMS key health."""
        kms_client = boto3.client("kms", region_name=self.aws_region)

        try:
            key_metadata = kms_client.describe_key(KeyId=key_id)["KeyMetadata"]

            return {
                "key_id": key_id,
                "provider": "aws_kms",
                "status": "healthy"
                if key_metadata["KeyState"] == "Enabled"
                else "unhealthy",
                "key_state": key_metadata["KeyState"],
                "enabled": key_metadata["KeyState"] == "Enabled",
                "rotation_enabled": key_metadata.get("KeyRotationEnabled", False),
                "last_rotation_date": key_metadata.get("KeyRotationStatus", {}).get(
                    "LastRotatedDate"
                ),
                "next_rotation_date": key_metadata.get("KeyRotationStatus", {}).get(
                    "NextRotatedDate"
                ),
                "checked_at": datetime.utcnow().isoformat() + "Z",
            }
        except ClientError as e:
            return {
                "key_id": key_id,
                "provider": "aws_kms",
                "status": "error",
                "error": str(e),
                "checked_at": datetime.utcnow().isoformat() + "Z",
            }

    def _get_gcp_key_health(self, key_name: str) -> Dict:
        """Get GCP KMS key health (placeholder)."""
        return {
            "key_name": key_name,
            "provider": "gcp_kms",
            "status": "unknown",
            "note": "GCP KMS health check requires specific implementation",
            "checked_at": datetime.utcnow().isoformat() + "Z",
        }

    def _get_azure_key_health(self, key_id: str) -> Dict:
        """Get Azure Key Vault key health (placeholder)."""
        return {
            "key_id": key_id,
            "provider": "azure_keyvault",
            "status": "unknown",
            "note": "Azure Key Vault health check requires specific implementation",
            "checked_at": datetime.utcnow().isoformat() + "Z",
        }
