from google.cloud import vision
from vision_client import get_vision_client
from vision_models import ImageDetectionRequest, ImageDescriptionResponse


def describe_image(request: ImageDetectionRequest) -> ImageDescriptionResponse:
    client = get_vision_client()
    image = vision.Image(content=request.image_content)
    # Google Cloud Vision's label detection can be used to infer a description
    response = client.label_detection(image=image)
    descriptions = [label.description for label in response.label_annotations]
    # Simple concatenation for demonstration. A more sophisticated approach would use an LLM.
    description_text = (
        "An image featuring: " + ", ".join(descriptions)
        if descriptions
        else "An image."
    )
    return ImageDescriptionResponse(description=description_text)
