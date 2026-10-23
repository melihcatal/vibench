import boto3


def extract_fields(document):
    client = boto3.client("textract")
    response = client.analyze_document(
        Document={"Bytes": document}, FeatureTypes=["FORMS"]
    )
    fields = response["Blocks"]
    return fields
