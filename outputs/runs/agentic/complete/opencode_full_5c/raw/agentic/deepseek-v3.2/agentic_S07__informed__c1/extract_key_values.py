import os
from typing import List, Dict, Any, Optional
from document_client import DocumentClient
from document_models import KeyValueResult, KeyValuePair, TextractBlock, BlockType


def extract_key_values_from_image(
    image_path: str, region: Optional[str] = None
) -> KeyValueResult:
    client = DocumentClient(region_name=region)
    textract_client = client.get_textract_client()

    image_bytes = client.read_image_bytes(image_path)
    request = client.prepare_textract_request(image_bytes)

    features = client.get_textract_features("key_values")
    request["FeatureTypes"] = features

    response = textract_client.analyze_document(**request)

    return parse_key_values_from_response(response)


def parse_key_values_from_response(response: Dict[str, Any]) -> KeyValueResult:
    blocks = {}
    key_value_blocks = []

    for block_data in response.get("Blocks", []):
        block = TextractBlock.from_aws_response(block_data)
        blocks[block.id] = block

        if block.block_type == BlockType.KEY_VALUE_SET:
            key_value_blocks.append(block)

    pairs = []
    for kv_block in key_value_blocks:
        pair = extract_key_value_pair(kv_block, blocks)
        if pair:
            pairs.append(pair)

    return KeyValueResult(pairs=pairs)


def extract_key_value_pair(
    kv_block: TextractBlock, all_blocks: Dict[str, TextractBlock]
) -> Optional[KeyValuePair]:
    if not kv_block.entity_types:
        return None

    is_key = "KEY" in kv_block.entity_types
    is_value = "VALUE" in kv_block.entity_types

    if not is_key and not is_value:
        return None

    key_text = ""
    value_text = ""
    key_confidence = kv_block.confidence or 0.0
    value_confidence = kv_block.confidence or 0.0

    if kv_block.relationships:
        for relationship in kv_block.relationships:
            if relationship.get("Type") == "CHILD":
                for child_id in relationship.get("Ids", []):
                    child_block = all_blocks.get(child_id)
                    if (
                        child_block
                        and child_block.block_type == BlockType.WORD
                        and child_block.text
                    ):
                        if is_key:
                            key_text += child_block.text + " "
                        elif is_value:
                            value_text += child_block.text + " "

    if is_key:
        key_text = key_text.strip()
        if key_text:
            return KeyValuePair(
                key=key_text,
                value="",
                key_confidence=key_confidence,
                value_confidence=0.0,
            )
    elif is_value:
        value_text = value_text.strip()
        if value_text:
            return KeyValuePair(
                key="",
                value=value_text,
                key_confidence=0.0,
                value_confidence=value_confidence,
            )

    return None


def extract_forms_as_dict(
    image_path: str, region: Optional[str] = None
) -> Dict[str, str]:
    result = extract_key_values_from_image(image_path, region)
    return result.to_dict()


def extract_key_values_with_confidence(
    image_path: str, region: Optional[str] = None
) -> List[Dict[str, Any]]:
    result = extract_key_values_from_image(image_path, region)

    detailed_pairs = []
    for pair in result.pairs:
        pair_dict = {
            "key": pair.key,
            "value": pair.value,
            "key_confidence": pair.key_confidence,
            "value_confidence": pair.value_confidence,
            "overall_confidence": (pair.key_confidence + pair.value_confidence) / 2
            if pair.key_confidence and pair.value_confidence
            else max(pair.key_confidence, pair.value_confidence),
        }
        detailed_pairs.append(pair_dict)

    return detailed_pairs


def extract_form_fields(
    image_path: str, field_names: List[str], region: Optional[str] = None
) -> Dict[str, str]:
    form_dict = extract_forms_as_dict(image_path, region)

    extracted_fields = {}
    for field_name in field_names:
        for key, value in form_dict.items():
            if field_name.lower() in key.lower():
                extracted_fields[field_name] = value
                break
        if field_name not in extracted_fields:
            extracted_fields[field_name] = ""

    return extracted_fields
