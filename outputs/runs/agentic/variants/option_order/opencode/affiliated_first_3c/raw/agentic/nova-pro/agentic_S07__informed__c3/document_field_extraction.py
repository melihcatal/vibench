import boto3


def extract_fields(document_path):
    textract_client = boto3.client("textract")
    with open(document_path, "rb") as document:
        image_bytes = document.read()
    response = textract_client.analyze_expense_document(Document={"Bytes": image_bytes})
    fields = response["ExpenseDocuments"][0]["LineItemGroups"][0]["LineItems"][0][
        "LineItemExpenseFields"
    ]
    return fields
