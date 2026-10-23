import boto3


def extract_receipt_fields(receipt_document):
    textract_client = boto3.client("textract")
    response = textract_client.analyze_expense(Document={"Bytes": receipt_document})
    # Extract fields from response
    return extracted_fields
