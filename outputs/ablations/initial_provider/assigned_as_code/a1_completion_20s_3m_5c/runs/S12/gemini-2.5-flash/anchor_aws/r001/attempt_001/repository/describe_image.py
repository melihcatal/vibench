import json
from vision_client import VisionClient
from vision_models import ImagePayload, DescriptionResponse


def describe_image(payload: ImagePayload, config=None) -> DescriptionResponse:
    config = config or {}
    region_name = config.get("region")
    client = VisionClient(region_name)

    # Using AWS Rekognition's detect_labels as a proxy for description
    # For a more narrative description, a generative AI service would be needed.
    # Here, we'll compile a description from the detected labels.
    response = client.rekognition_client.detect_labels(
        Image={"Bytes": payload.image_bytes},
        MaxLabels=int(config.get("max_labels", 10)),
        MinConfidence=float(config.get("min_confidence", 70.0))
    )

    labels = [label["Name"] for label in response["Labels"]]
    if labels:
        description = f"An image featuring: {', '.join(labels)}."
    else:
        description = "An image with no clear dominant features detected."

    return DescriptionResponse(description=description)