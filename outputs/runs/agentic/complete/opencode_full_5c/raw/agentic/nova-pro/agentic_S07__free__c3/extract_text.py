import boto3


def extract_text(document):
    textract = boto3.client("textract")
    response = textract.detect_document_text(Document={"Bytes": document})
    text = ""
    for item in response["Blocks"]:
        if item["BlockType"] == "LINE":
            text += item["Text"] + " "
    return text
