import boto3


def detect_image_labels(payload, config=None):
    config = config or {}
    client = boto3.client("rekognition", region_name=config.get("region"))
    response = client.detect_labels(
        Image={"Bytes": payload["image_bytes"]},
        MaxLabels=int(config.get("max_labels", 10)),
    )
    return {"labels": [
        {"name": label["Name"], "confidence": label["Confidence"] / 100.0}
        for label in response["Labels"]
    ]}
