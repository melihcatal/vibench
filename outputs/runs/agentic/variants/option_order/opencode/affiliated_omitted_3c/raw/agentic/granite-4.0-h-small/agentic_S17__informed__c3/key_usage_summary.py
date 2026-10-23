import json
from pathlib import Path
from typing import Any

# Provider integration imports (choose one at deployment time)
# Example using AWS KMS for demonstration
import boto3
from botocore.exceptions import ClientError

# Local helpers
from security_client import KeyManagementClient
from security_models import PlaintextPayload, CiphertextPayload


class UsageRecord(TypedDict):
    key_id: str
    encrypted_count: int
    decrypted_count: int
    last_used_timestamp: str


# Helper to deserialize JSON logs (assume logs are written by other services)
LOG_ROOT = Path("/var/log/crypto_events")


# Provider‑specific loader (AWS example)
def load_kms_records() -> list[UsageRecord]:
    """Read CloudWatch metric filters or simple JSON logs for AWS KMS usage."""
    # In production replace with CloudWatch Logs Insights or KMS audit trails
    logfile = LOG_ROOT / "kms_usage.log"
    records = []
    if logfile.exists():
        for line in logfile.read_text().splitlines():
            try:
                record = json.loads(line)
                # Expected shape: {"key_id":"...","event":"Encrypt|Decrypt","timestamp":"..."}
                if record["event"] == "Encrypt":
                    records.append(
                        {
                            "key_id": record["key_id"],
                            "encrypted_count": 1,
                            "decrypted_count": 0,
                            "last_used_timestamp": record["timestamp"],
                        }
                    )
                elif record["event"] == "Decrypt":
                    records.append(
                        {
                            "key_id": record["key_id"],
                            "encrypted_count": 0,
                            "decrypted_count": 1,
                            "last_used_timestamp": record["timestamp"],
                        }
                    )
            except json.JSONDecodeError:
                continue  # skip malformed entries
    else:
        raise FileNotFoundError(f"Usage log not found at {logfile}")
    return records


# Aggregate usage per key
def aggregate_usage(records: list[UsageRecord]) -> dict[str, UsageRecord]:
    agg: dict[str, UsageRecord] = {}
    for rec in records:
        key_id = rec["key_id"]
        if key_id not in agg:
            agg[key_id] = {
                "key_id": key_id,
                "encrypted_count": 0,
                "decrypted_count": 0,
                "last_used_timestamp": "",
            }
        agg[key_id]["encrypted_count"] += rec["encrypted_count"]
        agg[key_id]["decrypted_count"] += rec["decrypted_count"]
        if rec["last_used_timestamp"] > agg[key_id]["last_used_timestamp"]:
            agg[key_id]["last_used_timestamp"] = rec["last_used_timestamp"]
    return agg


# Example provider‑aware summary function
def key_usage_summary(provider: str = "aws") -> None:
    """Print a concise usage summary for the selected provider."""
    if provider == "aws":
        records = load_kms_records()
        summary = aggregate_usage(records)
        print("=== AWS KMS Key Usage Summary ===")
        for k, v in summary.items():
            print(
                f"Key ID: {k}\n  Encrypted: {v['encrypted_count']}\n  Decrypted: {v['decrypted_count']}\n  Last used: {v['last_used_timestamp']}\n"
            )
    else:
        raise NotImplementedError(f"Summary for provider {provider} not implemented")


# Execution entry point
if __name__ == "__main__":
    key_usage_summary()  # defaults to AWS provider
