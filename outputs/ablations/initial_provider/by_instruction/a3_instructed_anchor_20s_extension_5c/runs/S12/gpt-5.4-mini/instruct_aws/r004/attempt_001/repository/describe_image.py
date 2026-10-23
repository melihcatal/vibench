from vision_client import load_image_input, rekognition_client
from vision_models import VisionResult, normalize_labels


def describe_image(image_path: str) -> VisionResult:
    image = load_image_input(image_path)
    client = rekognition_client()
    response = client.detect_labels(Image={"Bytes": image.image_bytes}, MaxLabels=8, MinConfidence=60.0)
    labels = normalize_labels(
        [{"name": item.get("Name"), "confidence": float(item.get("Confidence", 0.0))} for item in response.get("Labels", [])]
    )
    description = ", ".join(label["name"] for label in labels[:3] if label.get("name"))
    return VisionResult(provider="aws.rekognition", kind="description", source=image.image_path, data={"description": f"Image likely contains {description}".strip()})
