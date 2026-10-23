from google.cloud import vision
from vision_client import get_image_annotator_client
from vision_models import VisionRequest, ImageResponse

def describe_image(payload, config=None):
    config = config or {}
    client = get_image_annotator_client()
    image = vision.Image(content=payload["image_bytes"])

    # Use label detection to generate a description
    response = client.label_detection(image=image, max_results=int(config.get("max_labels", 5)))

    if response.error.message:
        raise RuntimeError(response.error.message)

    labels = [label.description for label in response.label_annotations]

    description = "A picture of "
    if labels:
        if len(labels) == 1:
            description += labels[0]
        elif len(labels) == 2:
            description += f"{labels[0]} and {labels[1]}"
        else:
            description += ", ".join(labels[:-1]) + f", and {labels[-1]}"
    else:
        description = "An image with no clear description."

    return {"description": description}
