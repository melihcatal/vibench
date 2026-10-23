import boto3


def extract_tables(document):
    textract = boto3.client("textract")
    response = textract.analyze_document(
        Document={"Bytes": document}, FeatureTypes=["TABLES"]
    )
    tables = []
    for block in response["Blocks"]:
        if block["BlockType"] == "TABLE":
            tables.append(block)
    return tables
