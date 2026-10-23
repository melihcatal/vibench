import boto3
import json

# Amazon Textract AnalyzeExpense – integrates with AWS credentials
client = boto3.client("textract")


def extract_invoice_fields(file_path):
    # Call Textract AnalyzeExpense API
    response = client.analyze_expense(Document={"Bytes": open(file_path, "rb").read()})
    # Parse relevant fields
    expense = response["ExpenseDocuments"][0]
    vendor = None
    total = None
    date = None
    items = []
    for field in expense["ExpenseFields"]:
        label = field["LabelDetection"]
        value = field["ValueDetection"]
        if label.lower() == "vendor":
            vendor = value["Text"]
        elif label.lower() == "total":
            total = value["Text"]
        elif label.lower() == "invoice date":
            date = value["Text"]
        elif label.lower() == "item":
            items.append(value["Text"])
    return {"vendor": vendor, "date": date, "total": total, "items": items}
