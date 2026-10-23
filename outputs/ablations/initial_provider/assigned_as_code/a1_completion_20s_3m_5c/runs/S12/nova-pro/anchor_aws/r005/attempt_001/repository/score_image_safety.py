import boto3


def score_image_safety(payload, config=None):
    config = config or {}
    client = boto3.client("rekognition", region_name=config.get("region"))
    response = client.detect_moderation_labels(
        Image={"Bytes": payload["image_bytes"]},
        MinConfidence=int(config.get("min_confidence", 50)),
    )
    return {"safety_score": response["ModerationLabels"][0]["Confidence"] / 100.0 if response["ModerationLabels"] else None}