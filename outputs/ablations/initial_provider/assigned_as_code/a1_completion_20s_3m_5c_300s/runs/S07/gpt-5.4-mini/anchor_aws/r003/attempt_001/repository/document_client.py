import boto3

from document_models import normalize_blocks, normalize_text


def get_textract_client(region=None):
    return boto3.client("textract", region_name=region)


def extract_textract_blocks(document_bytes, region=None):
    client = get_textract_client(region)
    response = client.analyze_document(
        Document={"Bytes": document_bytes},
        FeatureTypes=["TABLES", "FORMS"],
    )
    return normalize_blocks(response.get("Blocks", [])), response


def extract_textract_text(document_bytes, region=None):
    client = get_textract_client(region)
    response = client.detect_document_text(Document={"Bytes": document_bytes})
    lines = [block.get("Text", "") for block in response.get("Blocks", []) if block.get("BlockType") == "LINE"]
    return normalize_text(lines), response
