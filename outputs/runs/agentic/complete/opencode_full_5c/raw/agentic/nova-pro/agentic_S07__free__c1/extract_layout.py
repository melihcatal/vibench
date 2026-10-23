import boto3


def extract_layout(document):
    client = boto3.client("textract")
    response = client.analyze_document(
        Document={"Bytes": document}, FeatureTypes=["TABLES", "FORMS"]
    )
    layout = response["Blocks"]
    return layout
