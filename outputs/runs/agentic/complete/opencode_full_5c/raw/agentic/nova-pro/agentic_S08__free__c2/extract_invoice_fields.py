import boto3


def extract_invoice_fields(document_path):
    textract = boto3.client("textract")
    with open(document_path, "rb") as document:
        response = textract.analyze_document(
            Document={"Bytes": document.read()}, FeatureTypes=["FORMS"]
        )
    # Extract fields
    vendor = None
    date = None
    total = None
    line_items = []
    for block in response["Blocks"]:
        if block["BlockType"] == "KEY_VALUE_PAIR":
            if block["Text"] == "Vendor":
                vendor = block["ValueDetection"]["Text"]
            elif block["Text"] == "Date":
                date = block["ValueDetection"]["Text"]
            elif block["Text"] == "Total":
                total = block["ValueDetection"]["Text"]
            elif block["Text"] == "Line Items":
                line_items = [
                    block["ValueDetection"]["Text"]
                    for block in response["Blocks"]
                    if block["BlockType"] == "LINE" and "Line Items" in block["Text"]
                ]
    return {"vendor": vendor, "date": date, "total": total, "line_items": line_items}
