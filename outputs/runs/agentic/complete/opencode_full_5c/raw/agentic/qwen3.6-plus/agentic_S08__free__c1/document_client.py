import os
import boto3
from botocore.config import Config


AWS_TEXTRACT_REGION = os.getenv("AWS_TEXTRACT_REGION", "us-east-1")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID", "")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY", "")
AWS_TEXTRACT_MAX_RETRIES = int(os.getenv("AWS_TEXTRACT_MAX_RETRIES", "3"))


def get_textract_client():
    session = boto3.Session(
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=AWS_TEXTRACT_REGION,
    )
    config = Config(
        retries={"max_attempts": AWS_TEXTRACT_MAX_RETRIES, "mode": "adaptive"}
    )
    client = session.client("textract", config=config)
    return client


def analyze_document_bytes(client, image_bytes):
    response = client.analyze_document(
        Document={"Bytes": image_bytes},
        FeatureTypes=["TABLES", "FORMS"],
    )
    return response


def analyze_document_s3(client, bucket, key):
    response = client.analyze_document(
        Document={"S3Object": {"Bucket": bucket, "Name": key}},
        FeatureTypes=["TABLES", "FORMS"],
    )
    return response


def parse_key_value_blocks(blocks):
    kv_map = {}
    key_map = {}
    value_map = {}
    for block in blocks:
        block_type = block.get("BlockType")
        if block_type == "KEY_VALUE_SET":
            entity_types = block.get("EntityTypes", [])
            if "KEY" in entity_types:
                key_map[block["Id"]] = block
            elif "VALUE" in entity_types:
                value_map[block["Id"]] = block

    for kid, kblock in key_map.items():
        key_text = _get_text_content(kblock, blocks)
        value_block_ids = kblock.get("Relationships", [{}])[0].get("Ids", [])
        value_text = ""
        confidence = 0.0
        for vid in value_block_ids:
            if vid in value_map:
                vblock = value_map[vid]
                value_text += _get_text_content(vblock, blocks) + " "
                confidence = max(confidence, vblock.get("Confidence", 0.0))
        kv_map[key_text.strip()] = {
            "value": value_text.strip(),
            "confidence": confidence / 100.0,
        }
    return kv_map


def parse_table_blocks(blocks):
    tables = []
    for block in blocks:
        if block.get("BlockType") == "TABLE":
            table_id = block["Id"]
            relationships = block.get("Relationships", [])
            cell_ids = []
            for rel in relationships:
                if rel.get("Type") == "CHILD":
                    cell_ids.extend(rel.get("Ids", []))
            cells = [
                b
                for b in blocks
                if b["Id"] in cell_ids and b.get("BlockType") == "CELL"
            ]
            rows = []
            row_map = {}
            for cell in cells:
                row_idx = cell.get("RowIndex", 1)
                col_idx = cell.get("ColumnIndex", 1)
                text = _get_text_content(cell, blocks)
                if row_idx not in row_map:
                    row_map[row_idx] = {}
                row_map[row_idx][col_idx] = text
            max_cols = max((max(r.keys()) for r in row_map.values()), default=0)
            for r_idx in sorted(row_map.keys()):
                row = []
                for c_idx in range(1, max_cols + 1):
                    row.append(row_map[r_idx].get(c_idx, ""))
                rows.append(row)
            tables.append(rows)
    return tables


def _get_text_content(block, blocks):
    text = ""
    relationships = block.get("Relationships", [])
    for rel in relationships:
        if rel.get("Type") == "CHILD":
            for child_id in rel.get("Ids", []):
                child_block = next((b for b in blocks if b["Id"] == child_id), None)
                if child_block:
                    text += child_block.get("Text", "") + " "
    return text.strip()
