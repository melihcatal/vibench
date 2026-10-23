import logging
from storage_client import TextractClient
from storage_models import DocumentOcrRequest, DocumentOcrResponse

logger = logging.getLogger(__name__)


def run_document_ocr(request: DocumentOcrRequest) -> DocumentOcrResponse:
    """Runs OCR on a stored document object in AWS S3 using Amazon Textract."""
    textract_client = TextractClient().get_client()

    try:
        response = textract_client.detect_document_text(
            Document={
                "S3Object": {"Bucket": request.bucket_name, "Name": request.object_key}
            }
        )

        text_detections = []
        for item in response.get("Blocks", []):
            if item["BlockType"] == "WORD":
                text_detections.append(item["Text"])

        logger.info(
            f"Successfully ran OCR on object {request.object_key} in bucket {request.bucket_name} using Amazon Textract."
        )
        return DocumentOcrResponse(text_detections=text_detections)
    except Exception as e:
        logger.error(
            f"Error running OCR on object {request.object_key} in bucket {request.bucket_name} with Textract: {e}"
        )
        raise
