from google.cloud import vision

from vision_client import load_vision_config, require_image_path


def describe_image(image_path: str) -> str:
    require_image_path(image_path)
    load_vision_config()
    client = vision.ImageAnnotatorClient()
    with open(image_path, "rb") as f:
        image = vision.Image(content=f.read())
    response = client.label_detection(image=image)
    labels = [x.description for x in response.label_annotations[:3]]
    return ", ".join(labels) if labels else "No clear visual description available."
