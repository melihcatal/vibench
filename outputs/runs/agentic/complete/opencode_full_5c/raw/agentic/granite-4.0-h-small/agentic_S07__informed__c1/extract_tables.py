from typing import List, Dict

# Table extraction model definitions (local helper)
Row = Dict[str, str]
Table = List[Row]

# Consolidated response across all table regions (local helper)
TableResult = List[Table]

# Amazon Textract table extraction integration
# Provider identifiable via boto3 SDK import


def extract_tables(image_bytes: bytes) -> TableResult:
    """Extract table cells and row structures from a document image with Textract."""
    client = boto3.client("textract")
    response = client.analyze_document(
        Document={"Bytes": image_bytes}, FeatureTypes=["TABLES"]
    )
    tables = []
    for table in response.get("Blocks", []):
        if table["BlockType"] == "TABLE":
            # Gather rows
            rows = []
            for child in table.get("Relationships", []):
                if child["Type"] == "CHILD":
                    for cell in child["Ids"]:
                        row_cells = {}
                        for child2 in client.get_block_details(cell):
                            if child2["BlockType"] == "CELL":
                                # naive mapping; real code would capture row/column indexes
                                row_cells[child2["ColumnIndex"]] = child2.get(
                                    "Text", ""
                                )
                        rows.append(row_cells)
            tables.append(rows)
    return tables
