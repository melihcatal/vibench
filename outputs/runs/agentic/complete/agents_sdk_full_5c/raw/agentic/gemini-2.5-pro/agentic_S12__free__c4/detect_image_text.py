from vision_client import get_aws_textract_client
from vision_models import ImageText

def detect_text(image_path: str) -> list[ImageText]:
    """
    Detects text in an image file using AWS Textract.

    Args:
        image_path: The path to the image file.

    Returns:
        A list of ImageText objects representing detected text lines.
    """
    textract_client = get_aws_textract_client()

    with open(image_path, 'rb') as image_file:
        image_bytes = image_file.read()

    response = textract_client.detect_document_text(
        Document={'Bytes': image_bytes}
    )

    detected_texts = []
    for item in response["Blocks"]:
        if item["BlockType"] == "LINE":
            detected_texts.append(
                ImageText(
                    text=item["Text"],
                    confidence=item["Confidence"] / 100.0,
                )
            )
    return detected_texts
