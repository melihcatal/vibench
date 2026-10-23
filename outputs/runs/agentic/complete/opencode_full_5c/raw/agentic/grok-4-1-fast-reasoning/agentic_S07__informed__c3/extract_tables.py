from document_client import create_textract_client, load_image_bytes
from typing import List, Dict


def _get_text(result_block: Dict, blocks: Dict) -> str:
    text = ""
    if "Relationships" in result_block:
        for relationship in result_block["Relationships"]:
            if relationship["Type"] == "CHILD":
                for word_id in relationship["Ids"]:
                    word = blocks[word_id]
                    if "Text" in word:
                        text += word["Text"] + " "
    return text.strip()


def extract_tables(image_path: str) -> List[List[List[str]]]:
    data = load_image_bytes(image_path)
    client = create_textract_client()
    response = client.analyze_document(
        Document={"Bytes": data}, FeatureTypes=["TABLES"]
    )
    blocks_map = {block["Id"]: block for block in response["Blocks"]}
    tables = []
    for block in response["Blocks"]:
        if block["BlockType"] == "TABLE":
            child_rel = next(
                (r for r in block["Relationships"] if r["Type"] == "CHILD"), None
            )
            if child_rel:
                cells = [blocks_map[child_id] for child_id in child_rel["Ids"]]
                row_map = {}
                for cell in cells:
                    top = cell["Geometry"]["BoundingBox"]["Top"]
                    row_key = round(top * 100)
                    if row_key not in row_map:
                        row_map[row_key] = []
                    row_map[row_key].append(cell)
                table_rows = []
                for row_key in sorted(row_map):
                    row_cells = sorted(
                        row_map[row_key],
                        key=lambda c: c["Geometry"]["BoundingBox"]["Left"],
                    )
                    row_texts = [_get_text(cell, blocks_map) for cell in row_cells]
                    table_rows.append(row_texts)
                tables.append(table_rows)
    return tables
