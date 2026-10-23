from google.cloud import vision

def describe_image(image_content: bytes) -> str:
    """
    Generates a short visual description for an image using Google Cloud Vision API.

    Args:
        image_content: The content of the image in bytes.

    Returns:
        A short visual description of the image.
    """
    client = vision.ImageAnnotatorClient()
    image = vision.Image(content=image_content)

    response = client.label_detection(image=image)
    labels = response.label_annotations

    if labels:
        description = ", ".join([label.description for label in labels])
        return f"The image depicts: {description}."
    else:
        return "No clear visual description could be generated for the image."

