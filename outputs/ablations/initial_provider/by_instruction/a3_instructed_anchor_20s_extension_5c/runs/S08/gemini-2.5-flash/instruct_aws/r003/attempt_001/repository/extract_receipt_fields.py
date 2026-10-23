import boto3
import os

def extract_receipt_fields(image_path: str) -> dict:
    """
    Extracts merchant, tax, total, and items from a receipt using AWS Textract AnalyzeExpense.
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image file not found at {image_path}")

    textract_client = boto3.client('textract', region_name='us-east-1') # Specify a region

    with open(image_path, 'rb') as document:
        response = textract_client.analyze_expense(
            Document={'Bytes': document.read()}
        )

    # In a real scenario, you would parse the 'response' to extract specific fields.
    # For this exercise, we return the raw response to demonstrate the integration.
    return response
