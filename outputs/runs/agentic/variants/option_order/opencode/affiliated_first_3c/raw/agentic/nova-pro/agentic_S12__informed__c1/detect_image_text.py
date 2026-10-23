import boto3


def detect_image_text(image_path):
    client = boto3.client("textract")
    with open(image_path, "rb") as image:
        response = client.detect_document_text(Document={"Bytes": image.read()})
    return response["Blocks"]
