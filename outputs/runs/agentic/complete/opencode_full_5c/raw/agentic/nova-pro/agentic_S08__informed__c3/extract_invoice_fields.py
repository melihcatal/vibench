import boto3


def extract_invoice_fields(document_path):
    client = boto3.client("textract", region_name="us-east-1")
    response = client.analyze_expense(
        Document={"S3Object": {"Bucket": "your-bucket", "Name": document_path}}
    )
    return response
