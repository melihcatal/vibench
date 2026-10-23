import os
import json
from vision_client import VisionClient


def detect_image_labels(image_path: str) -> dict:
    """Detect objects, labels, or concepts in a static image.

    This function uses Alibaba Cloud Vision (Image Search) as the concrete provider.
    The provider is identified by the SDK import `alibabacloud_vision` and the
    credentials read from environment variables.

    Args:
        image_path: Local file path to the image.

    Returns:
        A dict with keys:
            - 'labels': list of detected label strings
            - 'confidence': average confidence score
    """
    # Initialize the client – configuration is loaded from env vars by VisionClient
    client = VisionClient()
    # Call the provider’s label detection API
    response = client.detect_labels(image_path)
    # Normalize response to our simple format
    labels = response.get("labels", [])
    confidence = sum(item.get("score", 0) for item in response.get("items", [])) / len(
        response.get("items", 1)
    )
    return {"labels": labels, "confidence": confidence}


if __name__ == "__main__":
    # Example usage – replace with your own image path
    img = "example.jpg"
    result = detect_image_labels(img)
    print(json.dumps(result, ensure_ascii=False, indent=2))
