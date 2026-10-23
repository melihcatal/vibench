import boto3
import os
from storage_models import OcrDocumentRequest, OcrDocumentResponse


def run_ocr_on_document(request: OcrDocumentRequest) -> OcrDocumentResponse:
    textract_client = boto3.client(
        "textract",
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        region_name=os.environ.get("AWS_REGION", "us-east-1"),  # Default region
    )

    response = textract_client.detect_document_text(
        Document={
            "S3Object": {
                "Bucket": request.bucket_name,
                "Name": request.object_name,
            }
        }
    )

    full_text = []
    pages_data = []
    for block in response["Blocks"]:
        if block["BlockType"] == "LINE":
            full_text.append(block["Text"])
        if block["BlockType"] == "PAGE":
            pages_data.append(block)

    return OcrDocumentResponse(
        document_text="\n".join(full_text),
        pages=pages_data,
    )
