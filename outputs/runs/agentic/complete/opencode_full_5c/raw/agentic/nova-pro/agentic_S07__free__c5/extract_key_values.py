import boto3


def extract_key_values(document):
    textract = boto3.client("textract")
    response = textract.analyze_document(
        Document={"Bytes": document}, FeatureTypes=["FORMS"]
    )
    key_values = {}
    for block in response["Blocks"]:
        if block["BlockType"] == "KEY_VALUE_SET":
            key_values[block["KeyDetection"]["Text"]] = block["ValueDetection"]["Text"]
    return key_values
