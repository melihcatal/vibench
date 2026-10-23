from storage_client import StorageClient
from storage_models import StoredDocumentOCRRequest, StoredDocumentOCRResponse
import boto3
from botocore.exceptions import ClientError


def run_ocr_on_stored_document(
    request: StoredDocumentOCRRequest,
) -> StoredDocumentOCRResponse:
    textract_client = StorageClient().get_textract_client()
    try:
        # Start document text detection. For simplicity, using synchronous for now.
        # For large documents, asynchronous is recommended.
        response = textract_client.detect_document_text(
            Document={
                "S3Object": {"Bucket": request.bucket_name, "Name": request.object_key}
            }
        )

        text_content = []
        for item in response["Blocks"]:
            if item["BlockType"] == "LINE":
                text_content.append(item["Text"])

        return StoredDocumentOCRResponse(
            success=True,
            text_content="\n".join(text_content),
            message="OCR completed successfully.",
        )
    except ClientError as e:
        return StoredDocumentOCRResponse(
            success=False, message=f"Error running OCR: {e}"
        )
    except Exception as e:
        return StoredDocumentOCRResponse(
            success=False, message=f"An unexpected error occurred: {e}"
        )
