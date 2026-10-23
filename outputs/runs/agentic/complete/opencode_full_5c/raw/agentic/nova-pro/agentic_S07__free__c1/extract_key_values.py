import boto3


def extract_key_values(document):
    client = boto3.client("textract")
    response = client.analyze_document(
        Document={"Bytes": document}, FeatureTypes=["FORMS"]
    )
    key_values = response["Blocks"]
    return key_values
