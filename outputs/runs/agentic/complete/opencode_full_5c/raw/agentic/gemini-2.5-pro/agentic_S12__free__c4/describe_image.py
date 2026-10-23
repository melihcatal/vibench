from google.cloud import vision
from vision_client import get_vision_client
from vision_models import VisionRequest, VisionResponse, ImageDescription


def describe_image(request: VisionRequest) -> VisionResponse:
    """Generates a description for the image."""
    client = get_vision_client()
    image = vision.Image()
    image.source.image_uri = request.image_uri

    features = [vision.Feature(type_=vision.Feature.Type.IMAGE_PROPERTIES)]
    response = client.image_properties(image=image)
    # This is a simplification. A real implementation would use a more descriptive model.
    # For the sake of a clear example, we'll construct a simple description.
    # A better approach would be to use a specific image captioning model.
    # Google Cloud Vision's `TEXT_DETECTION` and `OBJECT_LOCALIZATION` could be
    # combined to generate a richer description.
    # For now, we will simulate a description from dominant colors.

    if response.image_properties_annotation.dominant_colors.colors:
        color = response.image_properties_annotation.dominant_colors.colors[0].color
        description_text = f"The image has a dominant color of RGB({color.red}, {color.green}, {color.blue})."
    else:
        description_text = "No description available."

    return VisionResponse(descriptions=[ImageDescription(text=description_text)])
