import boto3


def extract_tables(document):
    textract = boto3.client("textract")
    response = textract.analyze_document(
        Document={"Bytes": document}, FeatureTypes=["TABLES"]
    )
    tables = []
    for table in response["Blocks"]:
        if table["BlockType"] == "TABLE":
            tables.append(table)
    return tables
