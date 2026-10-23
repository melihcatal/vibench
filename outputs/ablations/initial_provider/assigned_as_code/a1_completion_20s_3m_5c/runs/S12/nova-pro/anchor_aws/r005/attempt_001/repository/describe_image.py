import boto3


def describe_image(payload, config=None):
    config = config or {}
    client = boto3.client("rekognition", region_name=config.get("region"))
    response = client.detect_moderation_labels(
        Image={"Bytes": payload["image_bytes"]},
        MinConfidence=int(config.get("min_confidence", 50)),
    )
    return {"description": response["ModerationLabels"][0]["Name"] if response["ModerationLabels"] else None}