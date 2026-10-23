import boto3

def check_safety(payload, config=None):
    config = config or {}
    client = boto3.client("comprehend", region_name=config.get("region"))
    response = client.detect_moderation_labels(Text=payload["text"])
    return {"moderation_labels": response["ModerationLabels"]}
