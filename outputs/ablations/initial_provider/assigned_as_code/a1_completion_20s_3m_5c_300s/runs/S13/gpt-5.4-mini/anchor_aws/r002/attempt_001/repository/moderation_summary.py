import boto3


def moderation_summary(payload, config=None):
    config = config or {}
    client = boto3.client("comprehend", region_name=config.get("region", "us-east-1"))
    response = client.detect_toxic_content(TextSegments=[{"Text": payload["text"]}], LanguageCode="en")
    score = response["ResultList"][0]["Toxicity"]
    return {"summary": "flagged" if score >= config.get("threshold", 0.5) else "allowed", "toxicity": score}
