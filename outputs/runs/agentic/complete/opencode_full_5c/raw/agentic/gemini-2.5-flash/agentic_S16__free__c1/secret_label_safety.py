import os
import json
from typing import Dict, Any
from security_client import SecretManagementClient

UNSAFE_KEYWORDS = [
    "password",
    "credential",
    "token",
    "secretkey",
    "api_key",
    "prod",
    "sensitive",
]


def check_secret_labels_for_safety(secret_id: str) -> Dict[str, Any]:
    client = SecretManagementClient()
    secret_metadata = client.get_secret_metadata(secret_id)

    safety_report = {
        "secret_id": secret_id,
        "labels_checked": {},
        "unsafe_keywords_found": [],
        "is_safe": True,
    }

    if not secret_metadata:
        safety_report["error"] = f"Secret {secret_id} not found."
        safety_report["is_safe"] = False
        return safety_report

    safety_report["secret_name"] = secret_metadata.name

    if secret_metadata.labels:
        for key, value in secret_metadata.labels.items():
            label_text = f"{key}:{value}".lower()
            found_unsafe = False
            for keyword in UNSAFE_KEYWORDS:
                if keyword in label_text:
                    safety_report["unsafe_keywords_found"].append(
                        f"Label '{key}' contains '{keyword}'"
                    )
                    found_unsafe = True
            safety_report["labels_checked"][key] = "UNSAFE" if found_unsafe else "SAFE"
            if found_unsafe:
                safety_report["is_safe"] = False
    else:
        safety_report["error"] = "No labels found for this secret."

    return safety_report


if __name__ == "__main__":
    # Example usage: Replace 'your-secret-id' with an actual secret ID
    # And ensure GOOGLE_CLOUD_PROJECT environment variable is set
    # Test with a secret that has labels like {"env": "prod", "owner": "security"}
    try:
        report = check_secret_labels_for_safety("your-secret-id-with-labels")
        print(json.dumps(report, indent=2))

        report_safe = check_secret_labels_for_safety(
            "your-safe-secret-id"
        )  # Assume no unsafe labels
        print(json.dumps(report_safe, indent=2))

    except Exception as e:
        print(f"An error occurred while checking secret labels: {e}")
