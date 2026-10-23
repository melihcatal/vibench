import boto3


def extract_layout(document):
    textract = boto3.client("textract")
    response = textract.analyze_document(
        Document={"Bytes": document}, FeatureTypes=["TABLES", "FORMS"]
    )
    layout = {
        "blocks": [],
        "lines": [],
        "tables": [],
    }
    for block in response["Blocks"]:
        if block["BlockType"] == "LINE":
            layout["lines"].append(block)
        elif block["BlockType"] == "TABLE":
            layout["tables"].append(block)
    return layout
