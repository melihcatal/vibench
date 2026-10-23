import os
import re
from typing import List
from security_client import SecretManagerHelper

# Google Cloud Project ID can be set as an environment variable
PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")


def check_secret_label_safety(secret_id: str) -> List[str]:
    if not PROJECT_ID:
        raise ValueError("GOOGLE_CLOUD_PROJECT_ID environment variable not set.")

    client = SecretManagerHelper(project_id=PROJECT_ID)
    metadata = client.get_secret_metadata(secret_id)

    unsafe_indicators = ["password", "key", "secret", "credential", "token"]
    unsafe_findings = []

    for label_key, label_value in metadata.labels.items():
        for indicator in unsafe_indicators:
            if re.search(
                r"\b" + re.escape(indicator) + r"\b", label_key, re.IGNORECASE
            ) or re.search(
                r"\b" + re.escape(indicator) + r"\b", label_value, re.IGNORECASE
            ):
                unsafe_findings.append(
                    f"Unsafe indicator '{indicator}' found in label: {label_key}={label_value}"
                )

    for annotation_key, annotation_value in metadata.annotations.items():
        for indicator in unsafe_indicators:
            if re.search(
                r"\b" + re.escape(indicator) + r"\b", annotation_key, re.IGNORECASE
            ) or re.search(
                r"\b" + re.escape(indicator) + r"\b", annotation_value, re.IGNORECASE
            ):
                unsafe_findings.append(
                    f"Unsafe indicator '{indicator}' found in annotation: {annotation_key}={annotation_value}"
                )

    return unsafe_findings


# Example Usage (replace with actual secret_id and set GOOGLE_CLOUD_PROJECT_ID env var)
if __name__ == "main":
    try:
        findings = check_secret_label_safety("my-secret-with-labels")
        if findings:
            print(f"Unsafe label/annotation findings for 'my-secret-with-labels':")
            for finding in findings:
                print(f"  - {finding}")
        else:
            print("No unsafe label/annotation findings.")
    except Exception as e:
        print(f"Error checking secret label safety: {e}")
