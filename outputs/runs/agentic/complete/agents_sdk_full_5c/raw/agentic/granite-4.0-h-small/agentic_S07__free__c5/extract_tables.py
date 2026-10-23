import os
from document_client import DocumentClient
from document_models import TableResponse

def extract_tables(image_path: str) -> list:
    """Extract table cells and row structure from a document using AWS Textract table analysis.
    
    Returns a list of tables, each table being a list of rows, each row a list of cell dicts.
    """
    client = DocumentClient()  # uses AWS credentials from env vars
    response = client.start_table_detection(image_path)
    # Poll for completion (simplified)
    tables = client.get_table_result(response["JobId"])
    return tables
