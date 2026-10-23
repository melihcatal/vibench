from vision_client import VisionClient
from vision_models import ImageDetectionRequest, ImageDescriptionResponse
from google.cloud import vision


def describe_image(request: ImageDetectionRequest) -> ImageDescriptionResponse:
    client = VisionClient().get_client()
    image = vision.Image()
    image.source.image_uri = request.image_uri

    response = client.web_detection(image=image)

    # Attempt to get a description from best guess labels or pages with matching images
    description = ""
    if response.web_detection.best_guess_labels:
        description = response.web_detection.best_guess_labels[0].label
    elif response.web_detection.visually_similar_images:
        # Fallback to the title of a visually similar image, if available
        for img in response.web_detection.visually_similar_images:
            if img.url:
                description = f"Visually similar to an image found online: {img.url}"
                break

    if not description and response.web_detection.full_matching_images:
        # Fallback to the title of a full matching image, if available
        for img in response.web_detection.full_matching_images:
            if img.page_title:
                description = img.page_title
                break

    if not description:
        # If still no description, try label detection as a last resort for some context
        label_response = client.label_detection(image=image)
        if label_response.label_annotations:
            description = label_response.label_annotations[0].description

    return ImageDescriptionResponse(
        description=description or "No specific visual description found."
    )
