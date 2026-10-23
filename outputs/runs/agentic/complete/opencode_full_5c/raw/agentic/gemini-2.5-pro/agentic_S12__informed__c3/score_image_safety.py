from google.cloud import vision
from vision_client import get_vision_client
from vision_models import ImageSafety


def score_image_safety(image_path: str) -> ImageSafety:
    client = get_vision_client()

    with open(image_path, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)
    response = client.safe_search_detection(image=image)
    safe_search = response.safe_search_annotation

    # Likelihood names are: 'UNKNOWN', 'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE',
    # 'LIKELY', 'VERY_LIKELY'.
    likelihood_name = (
        "UNKNOWN",
        "VERY_UNLIKELY",
        "UNLIKELY",
        "POSSIBLE",
        "LIKELY",
        "VERY_LIKELY",
    )

    return ImageSafety(
        adult=likelihood_name[safe_search.adult],
        spoof=likelihood_name[safe_search.spoof],
        medical=likelihood_name[safe_search.medical],
        violence=likelihood_name[safe_search.violence],
        racy=likelihood_name[safe_search.racy],
    )
