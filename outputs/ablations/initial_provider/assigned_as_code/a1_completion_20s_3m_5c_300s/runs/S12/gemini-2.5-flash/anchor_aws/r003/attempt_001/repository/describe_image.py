import boto3
from vision_client import get_rekognition_client
from vision_models import ImagePayload

def describe_image(payload: ImagePayload, config=None):
    config = config or {}
    client = get_rekognition_client(region_name=config.get("region"))
    response = client.detect_labels(
        Image={"Bytes": payload.image_bytes},
        MaxLabels=int(config.get("max_labels", 5)),
    )

    labels = [label["Name"] for label in response["Labels"] if label["Confidence"] > 70.0]
    if labels:
        description = "An image featuring " + ", ".join(labels) + "."
    else:
        description = "An image with no clear description."

    return {"description": description}
