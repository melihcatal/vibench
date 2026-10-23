import os
import json
from typing import Optional, Dict, Any, List
from datetime import datetime, timezone

from security_client import SecurityClient, KMSClientConfig, DEFAULT_KEY_ID
from security_models import KeyUsageSummary, KeyUsageEvent

AWS_KMS_REGION = os.environ.get(
    "AWS_DEFAULT_REGION", os.environ.get("AWS_REGION", "us-east-1")
)


def _describe_key(kms_client, key_id: str) -> Dict[str, Any]:
    response = kms_client.kms_client.describe_key(KeyId=key_id)
    key_metadata = response["KeyMetadata"]
    return {
        "key_id": key_metadata["KeyId"],
        "arn": key_metadata["Arn"],
        "key_state": key_metadata["KeyState"],
        "key_usage": key_metadata["KeyUsage"],
        "key_spec": key_metadata.get("KeySpec", "N/A"),
        "creation_date": key_metadata.get("CreationDate", "").isoformat()
        if isinstance(key_metadata.get("CreationDate"), datetime)
        else str(key_metadata.get("CreationDate", "")),
        "description": key_metadata.get("Description", ""),
        "origin": key_metadata.get("Origin", "AWS_KMS"),
    }


def _list_key_policies(kms_client, key_id: str) -> List[str]:
    try:
        response = kms_client.kms_client.list_key_policies(KeyId=key_id)
        return response.get("PolicyNames", [])
    except Exception:
        return []


def _get_key_rotation_status(kms_client, key_id: str) -> bool:
    try:
        response = kms_client.kms_client.get_key_rotation_status(KeyId=key_id)
        return response.get("KeyRotationEnabled", False)
    except Exception:
        return False


def summarize_key_usage(
    key_id: Optional[str] = None,
    include_key_metadata: bool = True,
    include_policies: bool = False,
    include_rotation_status: bool = False,
    client: Optional[SecurityClient] = None,
) -> Dict[str, Any]:
    target_key_id = key_id or DEFAULT_KEY_ID
    if not target_key_id:
        raise ValueError(
            "No KMS key ID provided. Set DEFAULT_KMS_KEY_ID or pass key_id explicitly."
        )

    kms_client = client or SecurityClient()

    usage_summary = kms_client.get_usage_summary(key_id=target_key_id)

    result: Dict[str, Any] = {
        "key_id": target_key_id,
        "summary_timestamp": datetime.now(timezone.utc).isoformat(),
        "operation_counts": {
            "total": usage_summary.total_operations,
            "encrypt": usage_summary.encrypt_count,
            "decrypt": usage_summary.decrypt_count,
            "sign": usage_summary.sign_count,
            "verify": usage_summary.verify_count,
            "generate_data_key": usage_summary.generate_data_key_count,
            "failed": usage_summary.failed_operations,
        },
        "success_rate": (
            round(
                (usage_summary.total_operations - usage_summary.failed_operations)
                / usage_summary.total_operations
                * 100,
                2,
            )
            if usage_summary.total_operations > 0
            else 100.0
        ),
    }

    if include_key_metadata:
        try:
            key_info = _describe_key(kms_client, target_key_id)
            result["key_metadata"] = key_info
        except Exception as exc:
            result["key_metadata_error"] = str(exc)

    if include_policies:
        try:
            policies = _list_key_policies(kms_client, target_key_id)
            result["key_policies"] = policies
        except Exception as exc:
            result["key_policies_error"] = str(exc)

    if include_rotation_status:
        try:
            rotation_enabled = _get_key_rotation_status(kms_client, target_key_id)
            result["key_rotation_enabled"] = rotation_enabled
        except Exception as exc:
            result["key_rotation_error"] = str(exc)

    if usage_summary.events:
        result["recent_events"] = [
            {
                "operation": e.operation,
                "timestamp": e.timestamp,
                "success": e.success,
                "error_message": e.error_message,
            }
            for e in usage_summary.events[-50:]
        ]

    return result


def summarize_all_tracked_usage(
    client: Optional[SecurityClient] = None,
) -> Dict[str, Any]:
    kms_client = client or SecurityClient()
    all_events = kms_client.get_usage_log()

    key_ids = list(set(e.key_id for e in all_events))
    per_key_summaries = {}
    for kid in key_ids:
        summary = kms_client.get_usage_summary(key_id=kid)
        per_key_summaries[kid] = {
            "total_operations": summary.total_operations,
            "encrypt_count": summary.encrypt_count,
            "decrypt_count": summary.decrypt_count,
            "sign_count": summary.sign_count,
            "verify_count": summary.verify_count,
            "generate_data_key_count": summary.generate_data_key_count,
            "failed_operations": summary.failed_operations,
        }

    total_ops = sum(s["total_operations"] for s in per_key_summaries.values())
    total_failures = sum(s["failed_operations"] for s in per_key_summaries.values())

    return {
        "summary_timestamp": datetime.now(timezone.utc).isoformat(),
        "total_keys_used": len(key_ids),
        "total_operations": total_ops,
        "total_failures": total_failures,
        "overall_success_rate": (
            round((total_ops - total_failures) / total_ops * 100, 2)
            if total_ops > 0
            else 100.0
        ),
        "per_key_summaries": per_key_summaries,
    }
