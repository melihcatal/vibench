# [LATER-STEP] rotation_summary.py
# Summarize secret rotation status across services

import json
from collections import defaultdict
from fetch_api_key import fetch_api_key
from fetch_db_secret import fetch_db_secret
from rotate_secret_version import rotate_secret_version


def summarize_rotations() -> str:
    """Collect current status of secret rotations and generate a summary.

    Returns:
        A formatted string summarizing rotation health per secret.
    """
    summary = defaultdict(list)
    # Example secrets to check (replace with real inventory)
    secrets = [
        {"name": "api-key", "path": "secret/api/api-key"},
        {
            "name": "db-credentials",
            "arn": "arn:aws:secretsmanager:us-east-1:123456789012:secret:db-creds",
        },
        {"name": "key-vault-secret", "name": "prod-key", "version": "staged"},
    ]

    for sec in secrets:
        if "path" in sec:
            # Vault API Key example
            try:
                key = fetch_api_key(sec["path"])
                summary[sec["name"]].append(
                    f"Vault API key fetched successfully. Version: latest"
                )
            except Exception as e:
                summary[sec["name"]].append(f"Vault fetch failed: {e}")
        elif "arn" in sec:
            # AWS Secrets Manager example
            try:
                db_cred = fetch_db_secret(sec["arn"])
                summary[sec["name"]].append(
                    f"AWS secret retrieved. Username: {db_cred.get('username')}"
                )
            except Exception as e:
                summary[sec["name"]].append(f"AWS secret fetch failed: {e}")
        elif "version" in sec:
            # Azure Key Vault rotation example
            try:
                val = rotate_secret_version(sec["name"], sec["version"])
                summary[sec["name"]].append(
                    f"Azure secret version {sec['version']} retrieved."
                )
            except Exception as e:
                summary[sec["name"]].append(f"Azure rotation failed: {e}")

    # Assemble report
    report_lines = ["=== Secret Rotation Summary ==="]
    for name, details in summary.items():
        report_lines.append(f"\nSecret: {name}")
        for detail in details:
            report_lines.append(f"  - {detail}")
    return "\n".join(report_lines)
