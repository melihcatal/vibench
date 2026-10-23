import boto3


def extract_receipt_fields(document_path):
    textract = boto3.client("textract")
    with open(document_path, "rb") as document:
        response = textract.analyze_document(
            Document={"Bytes": document.read()}, FeatureTypes=["FORMS"]
        )
    # Extract fields
    merchant = None
    tax = None
    total = None
    items = []
    for block in response["Blocks"]:
        if block["BlockType"] == "KEY_VALUE_PAIR":
            if block["Text"] == "Merchant":
                merchant = block["ValueDetection"]["Text"]
            elif block["Text"] == "Tax":
                tax = block["ValueDetection"]["Text"]
            elif block["Text"] == "Total":
                total = block["ValueDetection"]["Text"]
            elif block["Text"] == "Items":
                items = [
                    block["ValueDetection"]["Text"]
                    for block in response["Blocks"]
                    if block["BlockType"] == "LINE" and "Items" in block["Text"]
                ]
    return {"merchant": merchant, "tax": tax, "total": total, "items": items}
