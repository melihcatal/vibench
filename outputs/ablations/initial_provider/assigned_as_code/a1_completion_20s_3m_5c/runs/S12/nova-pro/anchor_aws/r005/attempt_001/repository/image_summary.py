import boto3


def image_summary(payload, config=None):
    config = config or {}
    client = boto3.client("rekognition", region_name=config.get("region"))
    labels_response = client.detect_labels(
        Image={"Bytes": payload["image_bytes"]},
        MaxLabels=int(config.get("max_labels", 10)),
    )
    text_response = client.detect_text(
        Image={"Bytes": payload["image_bytes"]},
    )
    labels = [label["Name"] for label in labels_response["Labels"]]
    text = [text_detection["DetectedText"] for text_detection in text_response["TextDetections"]]
    return {"summary": f"Labels: {labels}, Text: {text}"}