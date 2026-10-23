import boto3


def extract_layout(image_path):
    textract = boto3.client("textract")
    with open(image_path, "rb") as image:
        response = textract.detect_document_text(Document={"Bytes": image.read()})
    return response["Blocks"]
