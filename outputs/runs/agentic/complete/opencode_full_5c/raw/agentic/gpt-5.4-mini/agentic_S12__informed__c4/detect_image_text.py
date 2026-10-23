from vision_client import get_rekognition_client, read_image_bytes
from vision_models import VisionTextRequest, normalize_text_response


def detect_image_text(request: VisionTextRequest):
    client = get_rekognition_client()
    response = client.detect_text(Image={"Bytes": read_image_bytes(request.image_path)})
    text = " ".join(
        [
            item.get("DetectedText", "")
            for item in response.get("TextDetections", [])
            if item.get("Type") == "LINE"
        ]
    )
    return normalize_text_response(text)
