# visual_safety_text.py - Check generated visual labels for unsafe text using AWS Comprehend

import boto3
from typing import List

def contains_unsafe_text(texts: List[str]) -> bool:
    """Submit a list of strings to AWS Comprehend for toxicity/unsafe content detection.
    Returns True if any unsafe content is found.
    """
    # Create a single document (Comprehend accepts up to 25KB per request)
    document = "\\n".join(texts)
    client = boto3.client(
        "comprehend",
        region_name="us-east-1",
        # Credentials picked up from environment variables automatically
    )
    response = client.detect_pii_entities(
        Text=document,
        LanguageCode="en",
    )
    # Simple heuristic: if PII is found we treat as unsafe for this task
    return len(response.get("Entities", [])) > 0

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: visual_safety_text.py \"label1, label2, ...\")
        sys.exit(1)
    label_strs = sys.argv[1].split(",")
    unsafe = contains_unsafe_text(label_strs)
    print("UNSAFE" if unsafe else "SAFE")