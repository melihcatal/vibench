from vision_client import get_rekognition_client
from vision_models import ImageLabel


def detect_image_labels(image_bytes: bytes) -> list[ImageLabel]:
    rekognition = get_rekognition_client()
    response = rekognition.detect_labels(
        Image={"Bytes": image_bytes},
        MaxLabels=10,
    )

    labels = []
    if "Labels" in response:
        for label_data in response["Labels"]:
            labels.append(
                ImageLabel(
                    name=label_data["Name"], confidence=label_data["Confidence"] / 100.0
                )
            )

    return labels
