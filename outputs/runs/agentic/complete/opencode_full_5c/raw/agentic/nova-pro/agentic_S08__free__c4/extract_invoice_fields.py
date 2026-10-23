import boto3


def extract_invoice_fields(document):
    textract = boto3.client("textract")
    response = textract.analyze_document(
        Document={"Bytes": document}, FeatureTypes=["FORMS"]
    )
    invoice_fields = {}
    for block in response["Blocks"]:
        if block["BlockType"] == "KEY_VALUE_SET":
            if "KEY" in block["Text"]:
                key = block["Text"].replace("KEY", "").strip()
                value = block["Text"].replace("VALUE", "").strip()
                invoice_fields[key] = value
    return invoice_fields
