import boto3
from document_client import load_image, AWS_REGION
from document_models import parse_layout_blocks


def extract_layout(image_path: str) -> dict:
    image_bytes = load_image(image_path)
    textract = boto3.client("textract", region_name=AWS_REGION)
    response = textract.analyze_document(
        Document={"Bytes": image_bytes}, FeatureTypes=["LAYOUT"]
    )
    blocks = response["Blocks"]
    layout = parse_layout_blocks(blocks)
    return {"blocks": layout}
