import boto3
from document_client import load_image, AWS_REGION
from document_models import parse_ocr_text


def extract_text(image_path: str) -> dict:
    image_bytes = load_image(image_path)
    textract = boto3.client("textract", region_name=AWS_REGION)
    response = textract.detect_document_text(Document={"Bytes": image_bytes})
    blocks = response["Blocks"]
    lines = parse_ocr_text(blocks)
    text = "\n".join(lines)
    return {"text": text, "lines": lines}
