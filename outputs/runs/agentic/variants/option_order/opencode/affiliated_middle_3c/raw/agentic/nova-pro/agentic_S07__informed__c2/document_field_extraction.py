import boto3


def extract_fields(text):
    textract = boto3.client("textract")
    response = textract.analyze_document(
        Document={"Text": text}, FeatureTypes=["FORMS"]
    )
    fields = {}
    for block in response["Blocks"]:
        if block["BlockType"] == "KEY_VALUE_PAIR":
            fields[block["Key"]["Text"]] = block["Value"]["Text"]
    return fields
