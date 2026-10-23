import boto3
from vision_models import ImageText

def detect_image_text(image_path: str) -> ImageText:
    textract = boto3.client("textract")
    with open(image_path, "rb") as f:
        img_bytes = f.read()
    response = textract.detect_document_text(Document={"Bytes": img_bytes})
    texts = [block["Text"] for block in response["Blocks"] if block["BlockType"] == "LINE"]
    return ImageText(texts=texts)