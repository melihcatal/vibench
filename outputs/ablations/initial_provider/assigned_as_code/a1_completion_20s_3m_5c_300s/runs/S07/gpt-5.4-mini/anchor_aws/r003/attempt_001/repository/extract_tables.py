from document_client import extract_textract_blocks


def extract_tables(payload, config=None):
    config = config or {}
    blocks, response = extract_textract_blocks(payload["document_bytes"], region=config.get("region"))
    tables = []
    current_table = None
    for block in blocks:
        if block.get("BlockType") == "TABLE":
            current_table = {"cells": [], "page": block.get("Page"), "confidence": block.get("Confidence")}
            tables.append(current_table)
        elif block.get("BlockType") == "CELL" and current_table is not None:
            current_table["cells"].append(
                {
                    "row": block.get("RowIndex"),
                    "column": block.get("ColumnIndex"),
                    "row_span": block.get("RowSpan"),
                    "column_span": block.get("ColumnSpan"),
                    "text": block.get("Text", ""),
                }
            )
    return {"tables": tables, "raw": response}
