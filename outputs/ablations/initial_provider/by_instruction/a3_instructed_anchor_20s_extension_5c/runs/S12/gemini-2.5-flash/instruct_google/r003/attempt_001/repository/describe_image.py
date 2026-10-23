from vision_client import get_vision_client
from vision_models import image_to_base64
from google.cloud import vision

def describe_image(image_path: str) -> str:
    client = get_vision_client()

    with open(image_path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)
    response = client.label_detection(image=image)

    descriptions = []
    if response.label_annotations:
        for i, label in enumerate(response.label_annotations):
            if i < 3:  # Take top 3 labels for a concise description
                descriptions.append(label.description)
            else:
                break

    if descriptions:
        return f"The image depicts: {', '.join(descriptions)}."
    else:
        return "No clear description could be generated for the image."
