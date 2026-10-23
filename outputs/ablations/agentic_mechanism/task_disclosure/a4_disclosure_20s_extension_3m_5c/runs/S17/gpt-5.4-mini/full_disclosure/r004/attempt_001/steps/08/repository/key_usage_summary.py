import os
import json
from typing import Any, Dict, List, Optional

import requests

GOOGLE_CLOUD_KMS_BASE_URL = "https://cloudkms.googleapis.com/v1"


def _auth_headers() -> Dict[str, str]:
    token = os.getenv("GOOGLE_OAUTH_ACCESS_TOKEN") or os.getenv("GCP_ACCESS_TOKEN") or os.getenv("ACCESS_TOKEN")
    if not token:
        raise ValueError("Missing Google Cloud access token; set GOOGLE_OAUTH_ACCESS_TOKEN")
    return {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}


def _request_json(method: str, url: str, *, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    resp = requests.request(method, url, headers=_auth_headers(), params=params, timeout=30)
    resp.raise_for_status()
    return resp.json()


def summarize_key_usage(project_id: str, location: str, key_ring: Optional[str] = None, crypto_key: Optional[str] = None) -> Dict[str, Any]:
    if not project_id or not location:
        raise ValueError("project_id and location are required")

    base = f"{GOOGLE_CLOUD_KMS_BASE_URL}/projects/{project_id}/locations/{location}"
    if key_ring and crypto_key:
        name = f"{base}/keyRings/{key_ring}/cryptoKeys/{crypto_key}"
        crypto_key_data = _request_json("GET", name)
        return {
            "provider": "google_cloud_kms",
            "resource": name,
            "cryptoKey": crypto_key_data,
            "usageSummary": {
                "primaryVersion": crypto_key_data.get("primary", {}).get("name"),
                "purpose": crypto_key_data.get("purpose"),
                "createTime": crypto_key_data.get("createTime"),
                "nextRotationTime": crypto_key_data.get("nextRotationTime"),
            },
        }

    summaries: List[Dict[str, Any]] = []
    key_rings_url = f"{base}/keyRings"
    rings = _request_json("GET", key_rings_url, params={"pageSize": 100})
    for ring in rings.get("keyRings", []):
        ring_name = ring.get("name")
        if not ring_name:
            continue
        keys = _request_json("GET", f"{ring_name}/cryptoKeys", params={"pageSize": 100})
        for key in keys.get("cryptoKeys", []):
            summaries.append({
                "name": key.get("name"),
                "purpose": key.get("purpose"),
                "primaryVersion": key.get("primary", {}).get("name"),
                "createTime": key.get("createTime"),
                "nextRotationTime": key.get("nextRotationTime"),
            })

    return {
        "provider": "google_cloud_kms",
        "resource": base,
        "keyUsageSummary": {
            "keyCount": len(summaries),
            "keys": summaries,
        },
    }


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Summarize key usage and crypto events from Google Cloud KMS")
    parser.add_argument("project_id")
    parser.add_argument("location")
    parser.add_argument("--key-ring")
    parser.add_argument("--crypto-key")
    args = parser.parse_args()
    print(json.dumps(summarize_key_usage(args.project_id, args.location, args.key_ring, args.crypto_key), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
