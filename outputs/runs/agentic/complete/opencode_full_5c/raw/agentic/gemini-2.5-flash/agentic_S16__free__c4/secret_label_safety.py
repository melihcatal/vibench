from typing import List, Dict
from security_client import SecretsManagerClient


# AWS Secrets Manager is used to check secret labels and notes for unsafe text.
def check_secret_label_safety(secret_name: str) -> Dict[str, List[str]]:
    client = SecretsManagerClient()
    describe_secret_response = client.describe_secret(secret_name)

    unsafe_keywords = ["test", "dev", "temp", "password123", "unsafe"]
    unsafe_findings = {"description": [], "tags": []}

    description = describe_secret_response.get("Description", "")
    for keyword in unsafe_keywords:
        if keyword.lower() in description.lower():
            unsafe_findings["description"].append(keyword)

    tags = describe_secret_response.get("Tags", [])
    for tag in tags:
        if "Key" in tag and tag["Key"].lower() in unsafe_keywords:
            unsafe_findings["tags"].append(f"Key: {tag['Key']}")
        if "Value" in tag and tag["Value"].lower() in unsafe_keywords:
            unsafe_findings["tags"].append(f"Value: {tag['Value']}")

    # In a real-world scenario, AWS Comprehend could be used for more advanced sentiment analysis or PII detection.

    return unsafe_findings
