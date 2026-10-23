from google.cloud import vision

def describe_image(image_content: bytes) -> str:
    """
    Generates a short visual description for an image using Google Cloud Vision AI.

    Args:
        image_content: The content of the image as bytes.

    Returns:
        A string containing a short visual description of the image.
    """
    client = vision.ImageAnnotatorClient()
    image = vision.Image(content=image_content)

    response = client.label_detection(image=image)
    labels = response.label_annotations

    if labels:
        description = ", ".join([label.description for label in labels])
        return f"The image contains: {description}."
    else:
        return "Could not generate a description for the image."
