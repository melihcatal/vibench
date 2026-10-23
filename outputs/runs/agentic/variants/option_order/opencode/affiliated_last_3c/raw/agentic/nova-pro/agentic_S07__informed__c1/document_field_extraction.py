import boto3


def extract_structured_fields(text):
    textract = boto3.client("textract")
    response = textract.analyze_document(
        Document={"Bytes": text.encode("utf-8")}, FeatureTypes=["FORMS"]
    )
    fields = response["Blocks"]
    return fields
