from google.cloud import vision
from vision_client import get_vision_client

def describe_image(image_content: bytes) -> str:
    """Generates a short visual description for an image using Google Cloud Vision AI."""
    client = get_vision_client()
    image = vision.Image(content=image_content)

    # Use a specific feature for image description, typically LABEL_DETECTION combined with text interpretation
    # or sometimes specific document text detection for more comprehensive scene understanding.
    # For a *short visual description*, label detection is often used as a proxy or as part of a larger model.
    # If there was a specific 'description' feature, it would be used. For now, we'll infer from labels.
    # A more advanced model like Vertex AI's multimodal might offer direct description.
    # For Vision AI, often it's done via combining labels or using OCR for scene text if relevant.
    # Let's use label detection as a primary source for "description" in this context.
    response = client.label_detection(image=image)
    labels = [label.description for label in response.label_annotations if label.description]

    if labels:
        return f"An image depicting {', '.join(labels[:3])}." # Simple description from top labels
    else:
        return "An image with no clear description available."
