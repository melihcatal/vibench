from vision_client import load_image_input, rekognition_client
from vision_models import VisionResult, normalize_text


def detect_image_text(image_path: str) -> VisionResult:
    image = load_image_input(image_path)
    client = rekognition_client()
    response = client.detect_text(Image={"Bytes": image.image_bytes})
    text = normalize_text(
        [
            {
                "text": item.get("DetectedText"),
                "confidence": float(item.get("Confidence", 0.0)),
                "type": item.get("Type"),
            }
            for item in response.get("TextDetections", [])
        ]
    )
    return VisionResult(provider="aws.rekognition", kind="text", source=image.image_path, data={"text": text})
