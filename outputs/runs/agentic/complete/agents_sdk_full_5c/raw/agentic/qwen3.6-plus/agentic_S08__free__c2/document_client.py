"""Provide local configuration and client helper utilities for Structured Document Extraction."""

import os
import json
from typing import Optional, Dict, Any
import boto3
from botocore.exceptions import ClientError


AWS_TEXTRACT_REGION = os.environ.get("AWS_TEXTRACT_REGION", "us-east-1")
AWS_ACCESS_KEY = os.environ.get("AWS_ACCESS_KEY_ID", "")
AWS_SECRET_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY", "")


def get_textract_client():
    return boto3.client(
        "textract",
        region_name=AWS_TEXTRACT_REGION,
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY
    )


def analyze_invoice_with_textract(
    textract_client,
    document_bytes: bytes,
    feature_types: Optional[list] = None
) -> Dict[str, Any]:
    if feature_types is None:
        feature_types = ["TABLES", "FORMS", "SIGNATURES"]
    try:
        response = textract_client.analyze_document(
            Document={"Bytes": document_bytes},
            FeatureTypes=feature_types
        )
        return response
    except ClientError as e:
        raise RuntimeError(f"AWS Textract analyze_document failed: {e}")


def analyze_expense_document_with_textract(
    textract_client,
    document_bytes: bytes
) -> Dict[str, Any]:
    try:
        response = textract_client.analyze_expense(
            Document={"Bytes": document_bytes}
        )
        return response
    except ClientError as e:
        raise RuntimeError(f"AWS Textract analyze_expense failed: {e}")


def parse_textract_blocks(response: Dict[str, Any]) -> Dict[str, Any]:
    extracted = {
        "text": "",
        "key_value_pairs": {},
        "tables": [],
        "lines": []
    }
    blocks = response.get("Blocks", [])
    line_texts = []

    for block in blocks:
        if block["BlockType"] == "LINE":
            line_texts.append(block.get("Text", ""))

    extracted["text"] = " ".join(line_texts)
    extracted["lines"] = line_texts

    for block in blocks:
        if block["BlockType"] == "KEY_VALUE_SET":
            if "KEY" in block.get("EntityTypes", []):
                key_text = _get_relationship_text(block, blocks, "CHILD")
                value_block_id = _get_relationship_target(block, "VALUE")
                value_text = _get_block_text_by_id(value_block_id, blocks)
                extracted["key_value_pairs"][key_text] = value_text

        if block["BlockType"] == "TABLE":
            table_data = _parse_table(block, blocks)
            extracted["tables"].append(table_data)

    return extracted


def _get_relationship_text(block, all_blocks, relation_type):
    text_parts = []
    for rel in block.get("Relationships", []):
        if rel.get("Type") == relation_type:
            for child_id in rel.get("Ids", []):
                for b in all_blocks:
                    if b["Id"] == child_id and b["BlockType"] == "WORD":
                        text_parts.append(b.get("Text", ""))
    return " ".join(text_parts)


def _get_relationship_target(block, relation_type):
    for rel in block.get("Relationships", []):
        if rel.get("Type") == relation_type:
            ids = rel.get("Ids", [])
            return ids[0] if ids else None
    return None


def _get_block_text_by_id(block_id, all_blocks):
    for b in all_blocks:
        if b["Id"] == block_id:
            if b["BlockType"] == "WORD":
                return b.get("Text", "")
            return _get_relationship_text(b, all_blocks, "CHILD")
    return ""


def _parse_table(table_block, all_blocks):
    rows = []
    for rel in table_block.get("Relationships", []):
        if rel.get("Type") == "CHILD":
            cell_blocks = [b for b in all_blocks if b["Id"] in rel.get("Ids", []) and b["BlockType"] == "CELL"]

    current_row = []
    sorted_cells = sorted(
        [b for b in all_blocks if b["Id"] in
         [rid for rel in table_block.get("Relationships", []) if rel["Type"] == "CHILD" for rid in rel.get("Ids", [])]],
        key=lambda c: (c.get("RowIndex", 0), c.get("ColumnIndex", 0))
    )
    current_row_idx = 0
    row_data = []
    for cell in sorted_cells:
        if cell["BlockType"] != "CELL":
            continue
        row_idx = cell.get("RowIndex", 0)
        if row_idx != current_row_idx:
            if row_data:
                rows.append(row_data)
            row_data = []
            current_row_idx = row_idx
        cell_text = _get_relationship_text(cell, all_blocks, "CHILD")
        row_data.append(cell_text)
    if row_data:
        rows.append(row_data)

    return rows


def build_textract_query_prompt(
    document_bytes: bytes,
    query_text: str
) -> Dict[str, Any]:
    return {
        "Document": {"Bytes": document_bytes},
        "FeatureTypes": ["QUERIES"],
        "QueriesConfig": {
            "Queries": [{"Text": query_text}]
        }
    }


def load_document_from_path(path: str) -> bytes:
    with open(path, "rb") as f:
        return f.read()
