import boto3


def extract_receipt_fields(document):
    textract = boto3.client("textract")
    response = textract.analyze_expense(Document={"Bytes": document})
    # Extract fields from response
    return {
        "merchant": "merchant_name",
        "tax": "tax",
        "total": "total",
        "items": "items",
    }
