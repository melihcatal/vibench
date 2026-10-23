from document_client import DocumentClient
from document_models import DocumentPayload, ExtractionResult
import os

def document_field_extraction(payload: DocumentPayload, config=None):
    config = config or {}
    region = config.get("region", os.environ.get("AWS_REGION", "us-east-1"))
    client_wrapper = DocumentClient(region_name=region)
    client = client_wrapper.get_textract_client()

    response = client.analyze_document(
        Document={
            "Bytes": payload.document_bytes
        },
        FeatureTypes=["FORMS"]
    )

    key_value_pairs = {}
    key_map = {}
    value_map = {}
    block_map = {block["Id"]: block for block in response["Blocks"]}

    for block in response["Blocks"]:
        if block["BlockType"] == "KEY_VALUE_SET":
            if "KEY" in block["EntityTypes"]:
                key_map[block["Id"]] = block
            else:
                value_map[block["Id"]] = block

    for block_id, key_block in key_map.items():
        value_block = None
        for relationship in key_block["Relationships"]:
            if relationship["Type"] == "VALUE":
                for value_id in relationship["Ids"]:
                    if value_id in value_map:
                        value_block = value_map[value_id]
                        break
        
        key_text = "".join([block_map[bid]["Text"] for bid in key_block["Relationships"][0]["Ids"] if block_map[bid]["BlockType"] == "WORD"])
        value_text = "" 
        if value_block:
            value_text = "".join([block_map[bid]["Text"] for bid in value_block["Relationships"][0]["Ids"] if block_map[bid]["BlockType"] == "WORD"])

        key_value_pairs[key_text] = value_text

    return ExtractionResult({"extracted_fields": key_value_pairs}).data
