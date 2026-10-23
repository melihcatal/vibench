# [SAME-SCENARIO] extract_tables.py

import os
from document_client import DocumentOcrClient

def extract_tables_from_image(image_path: str) -> list:
    """Extract table cells and row structure from a scanned document image.

    Uses Amazon Textract AnalyzeDocument (table analysis) to retrieve cell-level data.
    Environment variables:
        - AWS_ACCESS_KEY_ID
        - AWS_SECRET_ACCESS_KEY
        - AWS_REGION
    Returns a list of tables where each table is a list of rows and each row is a list of cell values.
    """
    client = DocumentOcrClient(service=\"textract\")
    response = client.analyze_document(image_path, feature=\"TABLES\")
    tables = []
    for block in response.get(\"Blocks\", []):
        if block.get(\"BlockType\") == \"TABLE\":
            table = []
            for row in block.get(\"Relationships\", []):
                if row.get(\"Type\") == \"CHILD\":
                    cells = []
                    for cell in row.get(\"Ids\", []):
                        cell_block = next((b for b in response.get(\"Blocks\", []) if b.get(\"Id\") == cell), None)
                        if cell_block and cell_block.get(\"BlockType\") == \"CELL\":
                            cells.append(cell_block.get(\"Text\", \"\"))
                    if cells:
                        table.append(cells)
            if table:
                tables.append(table)
    return tables
