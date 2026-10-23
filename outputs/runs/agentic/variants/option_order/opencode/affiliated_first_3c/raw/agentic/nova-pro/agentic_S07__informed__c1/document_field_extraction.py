import boto3


def extract_structured_fields(text):
    textract_client = boto3.client("textract")
    response = textract_client.analyze_expense_document(Document={"Text": text})
    structured_fields = response["Blocks"]
    return structured_fields
