from google.cloud import vision

from vision_client import get_vision_client, load_image_bytes


def describe_image(image_path: str) -> str:
    client = get_vision_client()
    image = vision.Image(content=load_image_bytes(image_path))
    response = client.document_text_detection(image=image)
    text = response.full_text_annotation.text.strip()
    if text:
        return text.splitlines()[0][:160]
    response = client.label_detection(image=image)
    labels = [label.description for label in response.label_annotations[:3]]
    return ", ".join(labels)
