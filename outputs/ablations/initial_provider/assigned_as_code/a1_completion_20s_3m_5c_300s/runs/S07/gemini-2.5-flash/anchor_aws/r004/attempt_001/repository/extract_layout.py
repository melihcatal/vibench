import boto3
from typing import List, Dict, Any
from document_client import DocumentClient
from document_models import DocumentPayload, LayoutExtractionResult, LayoutBlock

def extract_layout(payload: DocumentPayload, config: Dict[str, Any] = None) -> LayoutExtractionResult:
    config = config or {}
    client = DocumentClient(config).get_textract_client()

    response = client.analyze_document(
        Document={"Bytes": payload.document_bytes},
        FeatureTypes=["LAYOUT"]
    )

    blocks: List[LayoutBlock] = []
    for block in response.get("Blocks", []):
        if block["BlockType"] in ["PAGE", "LINE", "WORD", "TABLE", "CELL", "KEY_VALUE_SET", "QUERY", "QUERY_RESULT", "TITLE", "PARAGRAPH", "LIST", "FIGURE", "SECTION_HEADER"]:
            text = block.get("Text")
            geometry = block.get("Geometry", {})
            blocks.append(LayoutBlock(block_type=block["BlockType"], text=text, geometry=geometry))

    return LayoutExtractionResult(blocks=blocks)
