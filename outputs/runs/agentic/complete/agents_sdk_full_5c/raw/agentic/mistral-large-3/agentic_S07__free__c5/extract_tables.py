import os
from typing import Dict, Any, List
import requests
from document_client import get_document_client
from document_models import TableExtractionResponse, TableCell


def extract_tables(image_path: str) -> TableExtractionResponse:
    """
    Extract tables and their cell structures from a document using Amazon Textract.
    """
    import boto3
    
    textract = boto3.client(
        "textract",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_REGION", "us-east-1")
    )
    
    with open(image_path, "rb") as image_file:
        content = image_file.read()
    
    # Amazon Textract-specific request for table detection
    response = textract.analyze_document(
        Document={"Bytes": content},
        FeatureTypes=["TABLES"]
    )
    
    tables = []
    for block in response.get("Blocks", []):
        if block["BlockType"] == "TABLE":
            cells = []
            for relationship in block.get("Relationships", []):
                if relationship["Type"] == "CHILD":
                    for cell_id in relationship["Ids"]:
                        cell_block = next(b for b in response["Blocks"] if b["Id"] == cell_id)
                        cells.append(
                            TableCell(
                                text=cell_block.get("Text", ""),
                                row_index=cell_block.get("RowIndex", 0),
                                column_index=cell_block.get("ColumnIndex", 0),
                                bounding_box=cell_block.get("Geometry", {}).get("Polygon", [])
                            )
                        )
            tables.append({"cells": cells})
    
    return TableExtractionResponse(
        tables=tables,
        provider="amazon_textract",
        raw_response=response
    )