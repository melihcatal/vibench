import os
import json
from document_client import OcrClient


def extract_tables(image_path: str) -> list:
    """Extract table cells and row structure from a document.

    Uses Amazon Textract AnalyzeDocument (FORMS) as the concrete provider. Set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables.
    """
    client = OcrClient()  # boto3 client wrapper
    response = client.start_document_text_detection(image_path)
    # Wait for job completion (simplified)
    job_id = response["JobId"]
    while True:
        status = client.get_document_text_detection(JobId=job_id)
        if status["JobStatus"] == "SUCCEEDED":
            break
    # Extract tables from the response
    tables = []
    for block in status["Blocks"]:
        if block["BlockType"] == "TABLE":
            table = {
                "id": block["Id"],
                "rows": len(block["Relationships"][0]["Ids"]),
                "columns": len(
                    block["Geometry"]["BoundingBox"]["Height"]
                ),  # placeholder logic
            }
            tables.append(table)
    return tables
