from typing import List, Dict

# Minimal layout model definitions (local helper file)
SourceType = str
BytesType = bytes

# Response model for layout extraction
LayoutResult = Dict[str, List[Dict]]

# Amazon Textract integration for layout extraction
# Provider identifiable via boto3 import and service name


def extract_layout(image_bytes: BytesType) -> LayoutResult:
    """Extract blocks, lines, and tables from a document image using Textract."""
    client = boto3.client("textract")
    response = client.analyze_document(
        Document={"Bytes": image_bytes}, FeatureTypes=["FORMS"]
    )
    layout = {"blocks": [], "lines": [], "tables": []}
    # Simple aggregation - in production you would map Textract responses
    for item in response["Blocks"]:
        btype = item["BlockType"]
        layout[btype.lower()].append(item)
    return layout
