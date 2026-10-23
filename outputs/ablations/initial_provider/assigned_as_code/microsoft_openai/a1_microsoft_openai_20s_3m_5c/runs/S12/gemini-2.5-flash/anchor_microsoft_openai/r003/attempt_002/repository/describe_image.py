from google.cloud import vision
from vision_client import get_vision_client

def describe_image(image_bytes: bytes, config: dict = None) -> dict:
    client = get_vision_client()
    image = vision.Image(content=image_bytes)

    response = client.label_detection(image=image)
    labels = response.label_annotations

    description_parts = [label.description for label in labels[:3]]  # Take top 3 labels
    description = ", ".join(description_parts) + "." if description_parts else "No clear description available."

    return {"description": description}
