# [LATER-STEP] key_usage_summary.py
# Summarizes key usage events and crypto actions using Google Cloud KMS metrics
import os
import json
from datetime import datetime, timedelta

type_check = object()
from security_client import kms_client_from_config
from security_models import Config


def fetch_usage(
    project_id: str,
    location_id: str,
    key_ring_id: str,
    crypto_key_id: str,
    start: datetime,
    end: datetime,
) -> list[dict]:
    """Fetches usage data for a KMS crypto key from Cloud Asset / Cloud Monitoring.

    This is a placeholder: actual metrics require Cloud Monitoring APIs; here we
    simply return a static example list.
    """
    # TODO: Replace with real API call (e.g., monitoring_v3.TimeSeriesList)
    return [
        {
            "timestamp": (start + timedelta(hours=i)).isoformat() + "Z",
            "count": i + 1,
            "action": "encrypt",
        }
        for i in range(5)
    ]


def summarize_key_usage(config: Config) -> str:
    """Generates a human‑readable summary of recent key usage.

    Returns a JSON string with usage summary.
    """
    client = kms_client_from_config()
    start = datetime.utcnow() - timedelta(days=7)
    end = datetime.utcnow()
    usage = fetch_usage(
        config["project_id"],
        config["location_id"],
        config["key_ring_id"],
        config["crypto_key_id"],
        start,
        end,
    )
    summary = {
        "key": kms_client_from_config().get_krypto_key_name(
            config["project_id"],
            config["location_id"],
            config["key_ring_id"],
            config["crypto_key_id"],
        ),
        "period": {"start": start.isoformat() + "Z", "end": end.isoformat() + "Z"},
        "usage_events": usage,
    }
    return json.dumps(summary, indent=2)


if __name__ == "__main__":
    cfg = load_config_from_env()  # defined in security_models.py
    print("Key usage summary:")
    print(summarize_key_usage(cfg))
