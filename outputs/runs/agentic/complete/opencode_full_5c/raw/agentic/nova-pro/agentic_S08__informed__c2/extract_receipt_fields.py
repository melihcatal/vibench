import boto3


def extract_receipt_fields(receipt_path):
    client = boto3.client("textract")
    with open(receipt_path, "rb") as image:
        image_bytes = image.read()
    response = client.analyze_expense(Document={"Bytes": image_bytes})
    merchant = response["ExpenseDocuments"][0]["SummaryFields"][0]["GroupProperties"][
        0
    ]["Types"][0]["Text"]
    tax = response["ExpenseDocuments"][0]["SummaryFields"][1]["ValueDetection"]["Text"]
    total = response["ExpenseDocuments"][0]["SummaryFields"][2]["ValueDetection"][
        "Text"
    ]
    items = [
        item["LineItemGroups"][0]["LineItemCategories"][0]["LineItems"][0][
            "LineItemExpenseFields"
        ][0]["Text"]
        for item in response["ExpenseDocuments"]
    ]
    return {"merchant": merchant, "tax": tax, "total": total, "items": items}
