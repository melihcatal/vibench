import boto3


def extract_key_values(document):
    textract = boto3.client("textract")
    response = textract.analyze_document(
        Document={"Bytes": document}, FeatureTypes=["FORMS"]
    )
    key_values = {}
    for block in response["Blocks"]:
        if block["BlockType"] == "KEY_VALUE_SET":
            if "KEY" in block["EntityTypes"]:
                key_values[block["Text"]] = ""
            else:
                key_values[list(key_values.keys())[-1]] += block["Text"] + " "
    return key_values
