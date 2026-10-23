from google.cloud import vision
from vision_models import ImagePayload, ImageDescription
from vision_client import VisionClient

def describe_image(payload: ImagePayload, config: dict = None) -> ImageDescription:
    config = config or {}
    client = VisionClient().get_image_annotator_client()
    
    image = vision.Image(content=payload.image_bytes)
    response = client.label_detection(image=image, max_results=int(config.get("max_labels", 5)))

    if response.error.message:
        raise RuntimeError(response.error.message)

    labels = [label.description for label in response.label_annotations if label.score > 0.7]
    
    description_text = "An image showing " + ", ".join(labels) + "." if labels else "An image with no clear description."
    
    # Confidence can be averaged or taken from the highest score label if available
    confidence = sum([label.score for label in response.label_annotations]) / len(response.label_annotations) if response.label_annotations else 0.0

    return ImageDescription(description=description_text, confidence=confidence)
