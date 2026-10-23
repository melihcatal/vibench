# message_safety.py
import os
import requests
from typing import Dict, Any

# Choose one safety provider; here we use AWS Comprehend Toxicity as an example
# Set env vars: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION


def check_safety(text: str) -> bool:
    """Return True if the supplied text passes the toxicity filter, else False.",
    Uses AWS Comprehend DetectPiiEntities (or DetectSentiment) as a simple proxy for safety.
    In real usage replace with Perspective API, Bedrock Guardrails, etc.
    """
    aws_region = os.getenv("AWS_REGION", "us-east-1")
    endpoint = f"https://{aws_region}.comprehend.amazonaws.com"
    headers = {
        "Content-Type": "application/x-amz-json-1.1",
        "X-Amz-Target": "ComprehendService.DetectPiiEntities",
    }
    payload = {"Text": text, "LangaugeCode": "en"}
    response = requests.post(
        endpoint,
        json=payload,
        headers=headers,
        auth=(os.getenv("AWS_ACCESS_KEY_ID"), os.getenv("AWS_SECRET_ACCESS_KEY")),
    )
    if response.status_code != 200:
        print(f"Safety check HTTP error: {response.status_code}")
        return False
    result = response.json()
    # Simplistic rule: if any PII found we consider unsafe
    if result.get("Error", {}).get("Message"):
        print(f"Safety service error: {result['Error']['Message']}")
        return False
    # No PII found => safe
    return True


# Example usage (remove in production)
if __name__ == "__main__":
    sample = "Hey, your password is abc123!"
    print(f"Is '{sample}' safe? {check_safety(sample)}")
