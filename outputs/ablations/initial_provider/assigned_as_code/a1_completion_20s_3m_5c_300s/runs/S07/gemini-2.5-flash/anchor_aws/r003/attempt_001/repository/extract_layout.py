import boto3


def extract_layout(payload, config=None):
    config = config or {}
    client = boto3.client("textract", region_name=config.get("region"))
    response = client.analyze_document(
        Document={"Bytes": payload["document_bytes"]}, Features=["LAYOUT"]
    )
    layout_blocks = [
        b
        for b in response["Blocks"]
        if b["BlockType"] in ["PAGE", "SECTION_HEADER", "TITLE", "PARAGRAPH", "LIST", "TABLE", "KEY_VALUE_SET"]
    ]
    return {"layout_elements": layout_blocks}
