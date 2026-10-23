import boto3
from typing import List, Dict, Any
from document_client import DocumentClient
from document_models import DocumentPayload, KeyValueExtractionResult, KeyValue

def extract_key_values(payload: DocumentPayload, config: Dict[str, Any] = None) -> KeyValueExtractionResult:
    config = config or {}
    client = DocumentClient(config).get_textract_client()

    response = client.analyze_document(
        Document={"Bytes": payload.document_bytes},
        FeatureTypes=["FORMS"]
    )

    key_values: List[KeyValue] = []
    blocks_by_id = {block["Id"]: block for block in response.get("Blocks", [])}

    for block in response.get("Blocks", []):
        if block["BlockType"] == "KEY_VALUE_SET" and "KEY" in block["EntityTypes"]:
            key_text = ""
            value_text = ""
            key_geometry = {}
            value_geometry = {}

            # Extract key text and geometry
            for relationship in block.get("Relationships", []):
                if relationship["Type"] == "CHILD":
                    for child_id in relationship["Ids"]:
                        child_block = blocks_by_id.get(child_id)
                        if child_block and child_block["BlockType"] == "WORD":
                            key_text += child_block.get("Text", "") + " "
            key_text = key_text.strip()
            key_geometry = block.get("Geometry", {})

            # Extract value text and geometry
            for relationship in block.get("Relationships", []):
                if relationship["Type"] == "VALUE":
                    for value_id in relationship["Ids"]:
                        value_block = blocks_by_id.get(value_id)
                        if value_block and "VALUE" in value_block["EntityTypes"]:
                            value_geometry = value_block.get("Geometry", {})
                            for value_rel in value_block.get("Relationships", []):
                                if value_rel["Type"] == "CHILD":
                                    for word_id in value_rel["Ids"]:
                                        word_block = blocks_by_id.get(word_id)
                                        if word_block and word_block["BlockType"] == "WORD":
                                            value_text += word_block.get("Text", "") + " "
                            value_text = value_text.strip()

            if key_text or value_text:
                key_values.append(KeyValue(
                    key=key_text,
                    value=value_text,
                    key_geometry=key_geometry,
                    value_geometry=value_geometry
                ))

    return KeyValueExtractionResult(key_values=key_values)
