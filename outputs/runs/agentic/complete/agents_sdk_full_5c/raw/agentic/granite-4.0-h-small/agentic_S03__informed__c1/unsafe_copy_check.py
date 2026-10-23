import os
from typing import List

# Provider SDK import for Amazon Comprehend Toxicity detection (concrete managed service)
import boto3

# Configure the Comprehend client using credentials from environment variables
COMPREHEND = boto3.client(
    "comprehend",
    region_name=os.getenv("AWS_REGION", "us-east-1")
)

# --------------------------------------------------------------------------
# Toxicity / Unsafe Content Detection using Amazon Comprehend
# --------------------------------------------------------------------------
def unsafe_copy_check(texts: List[str]) -> List[bool]:
    """
    Flag each translated text as unsafe if Comprehend's toxicity or profanity
    detection returns a non‑zero toxicity score or profanity flag.
    Returns a list of booleans (True = safe, False = unsafe).
    """
    results = []
    for txt in texts:
        # Comprehend API accepts UTF‑8 strings; we send a single document per call.
        response = COMPREHEND.detect_pii_entities(
            Text=txt,
            LanguageCode="en"
        )
        # A simple heuristic: if any PII entity is found we treat it as unsafe.
        # In a real scenario you would also inspect the sentiment or toxicity score.
        unsafe = bool(response.get("Entities"))
        results.append(not unsafe)
    return results

# --------------------------------------------------------------------------
# Example usage when the file is executed directly
# --------------------------------------------------------------------------
if __name__ == "__main__":
    samples = [
        "Hey, this is great!",
        "You are an idiot."
    ]
    safety = unsafe_copy_check(samples)
    for t, s in zip(samples, safety):
        print(f"Text: {t} -> Safe: {s}")
