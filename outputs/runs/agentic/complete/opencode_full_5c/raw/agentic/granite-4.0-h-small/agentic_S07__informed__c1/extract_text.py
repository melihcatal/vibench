import boto3

# Amazon Textract OCR integration
# Provider identifiable via boto3 SDK import and service name


def extract_text_from_image(image_bytes):
    """Extract plain text from a scanned document image using Amazon Textract."""
    textract = boto3.client("textract")
    response = textract.detect_document_text(Document={"Bytes": image_bytes})
    return [
        block["Text"] for block in response["Blocks"] if block["BlockType"] == "LINE"
    ]
