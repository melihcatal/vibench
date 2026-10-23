import os
from typing import List, Dict, Any, Optional
from document_client import DocumentClient
from document_models import TextractBlock, BlockType


def extract_layout_from_image(
    image_path: str, region: Optional[str] = None
) -> List[TextractBlock]:
    client = DocumentClient(region_name=region)
    textract_client = client.get_textract_client()

    image_bytes = client.read_image_bytes(image_path)
    request = client.prepare_textract_request(image_bytes)

    features = client.get_textract_features("layout")
    request["FeatureTypes"] = features

    response = textract_client.analyze_document(**request)

    layout_blocks = []
    for block_data in response.get("Blocks", []):
        block = TextractBlock.from_aws_response(block_data)
        if block.block_type in [
            BlockType.PAGE,
            BlockType.LINE,
            BlockType.WORD,
            BlockType.TABLE,
            BlockType.CELL,
        ]:
            layout_blocks.append(block)

    return layout_blocks


def extract_layout_elements(
    image_path: str, region: Optional[str] = None
) -> Dict[str, List[TextractBlock]]:
    blocks = extract_layout_from_image(image_path, region)

    elements = {"pages": [], "lines": [], "words": [], "tables": [], "cells": []}

    for block in blocks:
        if block.block_type == BlockType.PAGE:
            elements["pages"].append(block)
        elif block.block_type == BlockType.LINE:
            elements["lines"].append(block)
        elif block.block_type == BlockType.WORD:
            elements["words"].append(block)
        elif block.block_type == BlockType.TABLE:
            elements["tables"].append(block)
        elif block.block_type == BlockType.CELL:
            elements["cells"].append(block)

    return elements


def get_layout_bounding_boxes(
    image_path: str, region: Optional[str] = None
) -> List[Dict[str, Any]]:
    blocks = extract_layout_from_image(image_path, region)

    bounding_boxes = []
    for block in blocks:
        if block.geometry and block.text:
            bbox = {
                "text": block.text,
                "type": block.block_type.value,
                "confidence": block.confidence,
                "bounding_box": block.geometry.get("BoundingBox", {}),
                "polygon": block.geometry.get("Polygon", []),
            }
            bounding_boxes.append(bbox)

    return bounding_boxes


def extract_layout_with_relationships(
    image_path: str, region: Optional[str] = None
) -> Dict[str, Any]:
    client = DocumentClient(region_name=region)
    textract_client = client.get_textract_client()

    image_bytes = client.read_image_bytes(image_path)
    request = client.prepare_textract_request(image_bytes)

    request["FeatureTypes"] = ["LAYOUT"]

    response = textract_client.analyze_document(**request)

    layout_data = {"blocks": [], "relationships": []}

    for block_data in response.get("Blocks", []):
        block = TextractBlock.from_aws_response(block_data)
        layout_data["blocks"].append(block)

        if block.relationships:
            for rel in block.relationships:
                relationship_info = {
                    "source_block": block.id,
                    "type": rel.get("Type"),
                    "target_blocks": rel.get("Ids", []),
                }
                layout_data["relationships"].append(relationship_info)

    return layout_data
