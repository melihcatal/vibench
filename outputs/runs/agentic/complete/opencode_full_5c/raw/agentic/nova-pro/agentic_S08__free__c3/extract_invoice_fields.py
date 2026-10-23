import boto3


def extract_invoice_fields(document):
    textract = boto3.client("textract")
    response = textract.analyze_document(
        Document={"Bytes": document}, FeatureTypes=["TABLES", "FORMS"]
    )
    invoice_fields = {"vendor": "", "date": "", "total": "", "line_items": []}
    for block in response["Blocks"]:
        if block["BlockType"] == "KEY_VALUE_SET":
            if block["Text"] == "Vendor":
                invoice_fields["vendor"] = block["ValueDetection"]["Text"]
            elif block["Text"] == "Date":
                invoice_fields["date"] = block["ValueDetection"]["Text"]
            elif block["Text"] == "Total":
                invoice_fields["total"] = block["ValueDetection"]["Text"]
        elif block["BlockType"] == "TABLE":
            for cell in block["Relationships"][0]["Ids"]:
                cell_block = next(b for b in response["Blocks"] if b["Id"] == cell)
                if cell_block["BlockType"] == "CELL":
                    invoice_fields["line_items"].append(cell_block["Text"])
    return invoice_fields
