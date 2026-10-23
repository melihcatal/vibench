import os
import requests

# -------------------------------------------------
# SAME-SCENARIO: extract_tables.py
# Extracts table cells and row structure from a document using AWS Textract
# -------------------------------------------------

AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
AWS_Textract_URL = f"https://{'textract'}.{AWS_REGION}.amazonaws.com"


def extract_tables_from_image(image_path: str) -> list:
    """Calls Textract to extract tables (cells, rows) from a scanned image.

    Args:
        image_path: Path to the scanned document image (PNG/JPEG).

    Returns:
        List of tables, each table is a dict with rows and cells.
    """
    with open(image_path, "rb") as f:
        image_bytes = f.read()

    payload = {"Document": {"Bytes": image_bytes}, "FeatureTypes": ["TABLES"]}
    headers = {
        "Content-Type": "application/x-amz-json-1.1",
        "X-Amz-Target": "Textract.AnalyzeDocument",
        "X-Amz-Client-Request-Token": os.getenv("AWS_REQUEST_ID", "").strip(),
    }
    response = requests.post(
        f"{AWS_Textract_URL}/AnalyzeDocument", json=payload, headers=headers, timeout=30
    )
    response.raise_for_status()
    result = response.json()
    tables = []
    for block in result.get("Blocks", []):
        if block.get("BlockType") == "TABLE":
            table = {"cells": [], "rows": []}
            for field in block.get("Relationships", []):
                if field["Type"] == "CHILD":
                    for child_id in field["Ids"]:
                        child_block = next(
                            (
                                b
                                for b in result.get("Blocks", [])
                                if b.get("Id") == child_id
                            ),
                            None,
                        )
                        if child_block and child_block.get("BlockType") == "CELL":
                            table["cells"].append(child_block)
            tables.append(table)
    return tables
