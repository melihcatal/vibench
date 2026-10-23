from google.cloud import vision
from vision_client import get_vision_client
from vision_models import ImageInput, ImageSafeSearchAnnotation
import base64

def score_image_safety(image_input: ImageInput) -> ImageSafeSearchAnnotation:
    """Checks an image for unsafe content using Google Cloud Vision Safe Search."""
    client = get_vision_client()
    image = vision.Image(content=base64.b64decode(image_input.image_content_base64))

    response = client.safe_search_detection(image=image)
    safe_search = response.safe_search_annotation

    return ImageSafeSearchAnnotation(
        adult=safe_search.adult.name,
        spoof=safe_search.spoof.name,
        medical=safe_search.medical.name,
        violence=safe_search.violence.name,
        racy=safe_search.racy.name
    )
