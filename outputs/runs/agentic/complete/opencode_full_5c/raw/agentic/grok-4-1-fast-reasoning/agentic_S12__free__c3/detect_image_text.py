import boto3
from vision_client import image_to_bytes
from vision_models import DetectedText


def detect_image_text(image_path: str) -> DetectedText:
    textract = boto3.client("textract")
    img_bytes = image_to_bytes(image_path)
    response = textract.detect_document_text(Document={"Bytes": img_bytes})
    text_blocks = [
        block["Text"] for block in response["Blocks"] if block["BlockType"] == "LINE"
    ]
    text = " ".join(text_blocks)
    return DetectedText(text=text)
