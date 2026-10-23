import boto3


def extract_invoice_fields(invoice_document):
    textract_client = boto3.client("textract")
    response = textract_client.analyze_expense(Document={"Bytes": invoice_document})
    # Extract fields from response
    return extracted_fields
