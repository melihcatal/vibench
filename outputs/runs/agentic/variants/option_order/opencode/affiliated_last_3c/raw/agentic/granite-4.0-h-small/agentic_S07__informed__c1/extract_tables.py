import os
from boto3 import client

# Amazon Textract for table extraction
# Provider identifiable by 'boto3' import and 'textract' client

# Load AWS credentials from environment variables
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")


def extract_tables_from_image(image_bytes: bytes) -> list:
    """Extract table cells and row structure from a document image using Amazon Textract.

    Args:
        image_bytes: Binary content of the scanned image.

    Returns:
        List of tables where each table is a list of rows and each row is a list of cell values.
    """
    textract = client(
        "textract",
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    )
    response = textract.analyze_document(
        Document={"Bytes": image_bytes}, FeatureTypes=["TABLES"]
    )
    tables = []
    for table in response.get("Blocks", []):
        if table.get("BlockType") != "TABLE":
            continue
        table_cells = []
        for cell in table.get("Relationships", []):
            if cell.get("Type") != "CHILD":
                continue
            for field in cell.get("Ids", []):
                cell_block = next(
                    (b for b in response["Blocks"] if b["Id"] == field), None
                )
                if cell_block and cell_block.get("BlockType") == "CELL":
                    text = next(
                        (
                            b["Text"]
                            for b in response["Blocks"]
                            if b["Id"]
                            == cell_block.get("Relationships", [{}])[0].get(
                                "Ids", [{}]
                            )[0]
                        ),
                        "",
                    )
                    table_cells.append(text)
        tables.append(table_cells)
    return tables
