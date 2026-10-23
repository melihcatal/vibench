import boto3

AWS_ACCESS_KEY_ID = "your_access_key_id"
AWS_SECRET_ACCESS_KEY = "your_secret_access_key"


def extract_invoice_fields(document_path):
    textract = boto3.client(
        "textract",
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    )
    with open(document_path, "rb") as document:
        response = textract.analyze_expense(Document={"Bytes": document.read()})
    return response
