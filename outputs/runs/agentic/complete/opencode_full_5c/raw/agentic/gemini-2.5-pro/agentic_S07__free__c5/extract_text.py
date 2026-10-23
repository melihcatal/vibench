from google.cloud import vision
from document_client import get_google_vision_client
from document_models import ExtractedText


def extract_text_from_image(image_path: str) -> ExtractedText:
    client = get_google_vision_client()
    with open(image_path, "rb") as image_file:
        content = image_file.read()
    image = vision.Image(content=content)
    response = client.document_text_detection(image=image)

    if response.error.message:
        raise Exception(
            "{}\nFor more info on error messages, check: "
            "https://cloud.google.com/apis/design/errors".format(response.error.message)
        )

    return ExtractedText(text=response.full_text_annotation.text)
