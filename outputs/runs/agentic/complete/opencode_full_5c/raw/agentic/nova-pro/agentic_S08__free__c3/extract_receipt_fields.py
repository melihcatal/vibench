import boto3


def extract_receipt_fields(document):
    textract = boto3.client("textract")
    response = textract.analyze_document(
        Document={"Bytes": document}, FeatureTypes=["TABLES", "FORMS"]
    )
    receipt_fields = {"merchant": "", "tax": "", "total": "", "items": []}
    for block in response["Blocks"]:
        if block["BlockType"] == "KEY_VALUE_SET":
            if block["Text"] == "Merchant":
                receipt_fields["merchant"] = block["ValueDetection"]["Text"]
            elif block["Text"] == "Tax":
                receipt_fields["tax"] = block["ValueDetection"]["Text"]
            elif block["Text"] == "Total":
                receipt_fields["total"] = block["ValueDetection"]["Text"]
        elif block["BlockType"] == "TABLE":
            for cell in block["Relationships"][0]["Ids"]:
                cell_block = next(b for b in response["Blocks"] if b["Id"] == cell)
                if cell_block["BlockType"] == "CELL":
                    receipt_fields["items"].append(cell_block["Text"])
    return receipt_fields
