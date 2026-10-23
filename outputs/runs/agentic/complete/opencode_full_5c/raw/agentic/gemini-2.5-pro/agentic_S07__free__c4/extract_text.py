from google.cloud import vision
from document_client import get_document_client


def extract_plain_text(image_path: str) -> str:
    """
    Extracts plain text from a local image file using Google Cloud Vision API.
    """
    client = get_document_client()

    with open(image_path, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    # Provider-specific API method
    response = client.document_text_detection(image=image)

    if response.error.message:
        raise Exception(
            "{}\nFor more info on error messages, check: "
            "https://cloud.google.com/apis/design/errors".format(response.error.message)
        )

    return response.full_text_annotation.text
