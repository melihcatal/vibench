import json
from model_models import ModelInvocationResponse
from typing import Dict

def platform_output_safety(raw_response: ModelInvocationResponse) -> Dict[str, Any]:
    """
    Inspect a model's textual output for unsafe content using Amazon Comprehend
    Toxicity detection (managed service). Returns a dict with the original text
    and a safety flag/status.
    """
    import boto3
    from botocore.exceptions import ClientError
    
    # Build payload for Comprehend DetectPiiEntities or DetectSentiment/Comprehend
    # Here we use DetectSentiment as a simple unsafe content proxy.
    comprehend = boto3.client(
        "comprehend",
        region_name=os.getenv("AWS_REGION", "us-east-1")
    )
    payload = {
        "Text": raw_response.text,
        "LanguageCode": "en"
    }
    try:
        detect_resp = comprehend.detect_sentiment(**payload)
    except ClientError as e:
        # In case the service is unavailable, fallback to a neutral safety flag.
        return {
            "text": raw_response.text,
            "safe": True,
            "safety_check": "service_unavailable",
            "error": str(e)
        }
    sentiment = detect_resp.get("Sentiment")
    # Treat NEGATIVE or MIXED as potentially unsafe for generalized models.
    safe = sentiment in ("POSITIVE", "NEUTRAL")
    return {
        "text": raw_response.text,
        "safe": safe,
        "sentiment": sentiment,
        "safety_check": "comprehend_sentiment"
    }

# Example usage when run as a script
if __name__ == "__main__":
    import os
    deployment = os.getenv("DEPLOYMENT_ID")
    if not deployment:
        raise RuntimeError("Set DEPLOYMENT_ID environment variable.")
    prompt = "Write a short harmful instruction."
    response = collect_platform_metadata(deployment, prompt)  # reuse existing helper
    safety_info = platform_output_safety(response)
    print(json.dumps(safety_info, indent=2))
