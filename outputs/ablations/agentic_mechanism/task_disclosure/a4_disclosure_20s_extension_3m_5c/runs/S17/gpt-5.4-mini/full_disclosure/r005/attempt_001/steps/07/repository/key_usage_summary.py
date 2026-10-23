import json
import os
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from google.cloud import kms_v1


def _dt(value: Any) -> Optional[str]:
    if value is None:
        return None
    if isinstance(value, datetime):
        if value.tzinfo is None:
            value = value.replace(tzinfo=timezone.utc)
        return value.astimezone(timezone.utc).isoformat()
    return str(value)


def summarize_key_usage(key_name: str, days: int = 30) -> Dict[str, Any]:
    client = kms_v1.KeyManagementServiceClient()
    key = client.get_crypto_key(request={"name": key_name})
    version_path = f"{key_name}/cryptoKeyVersions/-"
    page = client.list_crypto_key_versions(request={"parent": key_name})
    versions: List[Dict[str, Any]] = []
    for version in page:
        versions.append(
            {
                "name": version.name,
                "state": kms_v1.CryptoKeyVersion.CryptoKeyVersionState.Name(version.state),
                "algorithm": kms_v1.CryptoKeyVersion.CryptoKeyVersionAlgorithm.Name(version.algorithm),
                "protection_level": kms_v1.CryptoKeyVersion.ProtectionLevel.Name(version.protection_level),
                "create_time": _dt(version.create_time),
                "destroy_time": _dt(getattr(version, "destroy_time", None)),
            }
        )
    return {
        "provider": "google_cloud_kms",
        "key_name": key.name,
        "primary_version": getattr(key.primary.name, "", None) if getattr(key, "primary", None) else None,
        "versions": versions,
        "crypto_event_hint": {
            "resource": version_path,
            "window_days": days,
            "note": "Use Cloud Audit Logs for encrypt/decrypt/sign events tied to this key.",
        },
    }


def main() -> None:
    key_name = os.environ["GCP_KMS_KEY_NAME"]
    days = int(os.environ.get("SUMMARY_DAYS", "30"))
    print(json.dumps(summarize_key_usage(key_name=key_name, days=days), ensure_ascii=False))


if __name__ == "__main__":
    main()
