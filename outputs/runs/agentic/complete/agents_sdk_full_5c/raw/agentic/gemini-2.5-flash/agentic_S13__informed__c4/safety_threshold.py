import os
import boto3
import json

def get_safety_thresholds(secret_name: str = "safety_thresholds", region_name: str = "us-east-1"):
    """
    Retrieves safety thresholds from AWS Secrets Manager.
    """
    aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")

    client = boto3.client(
        "secretsmanager",
        region_name=region_name,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key
    )

    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
        if 'SecretString' in get_secret_value_response:
            return json.loads(get_secret_value_response['SecretString'])
        else:
            # Handle binary secret if needed
            print("Warning: Binary secret found, expected string for thresholds.")
            return {}
    except Exception as e:
        print(f"Error retrieving secret '{secret_name}' from AWS Secrets Manager: {e}")
        return {}

def apply_safety_threshold(moderation_result: dict, category_thresholds: dict):
    """
    Applies category thresholds to decide whether to allow text.
    Assumes moderation_result has keys like 'hate', 'sexual', 'violence', etc.
    and values representing severity levels (e.g., 0-4).
    """
    allowed = True
    reasons = []

    if not category_thresholds:
        print("Warning: No category thresholds provided or loaded. All text will be allowed by default.")
        return {"allowed": True, "reasons": ["No thresholds applied"]}

    for category, score in moderation_result.items():
        if category in category_thresholds:
            threshold = category_thresholds[category]
            if score >= threshold:
                allowed = False
                reasons.append(f"'{category}' score ({score}) exceeded threshold ({threshold})")
    
    return {"allowed": allowed, "reasons": reasons if reasons else ["Text allowed"]}
