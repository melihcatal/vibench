import boto3
from document_client import load_image, AWS_REGION
from document_models import parse_tables


def extract_tables(image_path: str) -> dict:
    image_bytes = load_image(image_path)
    textract = boto3.client("textract", region_name=AWS_REGION)
    response = textract.analyze_document(
        Document={"Bytes": image_bytes}, FeatureTypes=["TABLES"]
    )
    blocks = response["Blocks"]
    tables = parse_tables(blocks)
    return {"tables": tables}
