import boto3


def extract_layout(document):
    textract = boto3.client("textract")
    response = textract.analyze_document(
        Document={"Bytes": document}, FeatureTypes=["TABLES", "FORMS"]
    )
    layout = []
    for block in response["Blocks"]:
        if block["BlockType"] in ["CELL", "LINE", "WORD"]:
            layout.append(block)
    return layout
