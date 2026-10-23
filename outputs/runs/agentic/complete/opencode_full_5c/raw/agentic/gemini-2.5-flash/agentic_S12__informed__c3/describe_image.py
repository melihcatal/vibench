from google.cloud import vision
from vision_client import VisionClient
from vision_models import ImageAnalysisRequest, ImageDescription


def describe_image(request: ImageAnalysisRequest) -> ImageDescription:
    client = VisionClient().get_client()
    image = vision.Image()
    image.source.image_uri = request.image_uri

    response = client.web_detection(image=image)
    # Google Cloud Vision API does not have a direct 'describe image' feature like some LLMs.
    # For a short visual description, we can combine web entities or labels.
    # For this example, we'll use the first best guess entity label if available, otherwise a generic message.
    description_text = "No specific description available."
    if response.web_detection and response.web_detection.best_guess_labels:
        description_text = response.web_detection.best_guess_labels[0].label
    elif response.web_detection and response.web_detection.visually_similar_images:
        # Fallback to visually similar images if no best guess label
        description_text = f"Image visually similar to {len(response.web_detection.visually_similar_images)} others."

    return ImageDescription(text=description_text)
