import boto3
from document_client import load_image, AWS_REGION
from document_models import parse_key_values


def extract_key_values(image_path: str) -> dict:
    image_bytes = load_image(image_path)
    textract = boto3.client("textract", region_name=AWS_REGION)
    response = textract.analyze_document(
        Document={"Bytes": image_bytes}, FeatureTypes=["FORMS"]
    )
    blocks = response["Blocks"]
    key_values = parse_key_values(blocks)
    return {"key_values": key_values}
