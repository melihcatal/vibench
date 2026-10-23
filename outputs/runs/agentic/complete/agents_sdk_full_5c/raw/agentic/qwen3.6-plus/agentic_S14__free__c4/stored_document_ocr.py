"""Run OCR on a stored document object using AWS Textract."""

from typing import Optional

from storage_client import S3ClientFactory
from storage_models import OCRTaskRequest, OCRResult


def run_ocr_on_stored_document(
    key: str,
    bucket: Optional[str] = None,
    document_type: str = "application/pdf",
) -> OCRResult:
    """
    Perform OCR on a document stored in S3 using AWS Textract.

    Calls the AWS Tetect AnalyzeDocument or StartDocumentTextDetection API
    against the Textract service endpoint (textract.us-east-1.amazonaws.com)
    to extract text from PDF, TIFF, PNG, or JPEG documents stored in S3.

    Args:
        key: S3 object key of the document to process.
        bucket: S3 bucket name (falls back to S3_BUCKET_NAME env var).
        document_type: MIME type of the document
                       (application/pdf, image/png, image/jpeg, image/tiff).

    Returns:
        OCRResult containing extracted text, confidence scores, and block data.

    Raises:
        botocore.exceptions.ClientError: If Textract cannot access the S3 object
            or the document format is unsupported.
    """
    factory = S3ClientFactory(bucket=bucket)
    target_bucket = factory.bucket

    textract_client = factory.get_textract_client()

    is_pdf = document_type == "application/pdf"

    if is_pdf:
        response = textract_client.start_document_text_detection(
            DocumentLocation={
                "S3Object": {
                    "Bucket": target_bucket,
                    "Name": key,
                }
            }
        )
        job_id = response.get("JobId")

        result_blocks = _poll_textract_job(textract_client, job_id)
    else:
        response = textract_client.detect_document_text(
            Document={
                "S3Object": {
                    "Bucket": target_bucket,
                    "Name": key,
                }
            }
        )
        result_blocks = response.get("Blocks", [])

    return _parse_textract_blocks(result_blocks, key)


def run_ocr_on_stored_document_sync(
    key: str,
    bucket: Optional[str] = None,
) -> OCRResult:
    """
    Perform synchronous OCR on a single-page image stored in S3.

    Uses AWS Textract's detect_document_text API for quick, synchronous
    text extraction from image documents (PNG, JPEG, TIFF) stored in S3.

    Args:
        key: S3 object key of the image document.
        bucket: S3 bucket name.

    Returns:
        OCRResult with extracted text and per-word confidence.
    """
    factory = S3ClientFactory(bucket=bucket)
    target_bucket = factory.bucket

    textract_client = factory.get_textract_client()

    response = textract_client.detect_document_text(
        Document={
            "S3Object": {
                "Bucket": target_bucket,
                "Name": key,
            }
        }
    )

    blocks = response.get("Blocks", [])
    return _parse_textract_blocks(blocks, key)


def _poll_textract_job(textract_client, job_id: str, max_wait: int = 120) -> list:
    """Poll AWS Textract until the document analysis job completes."""
    import time

    start = time.time()
    while time.time() - start < max_wait:
        response = textract_client.get_document_text_detection(JobId=job_id)
        status = response.get("JobStatus", "")

        if status == "SUCCEEDED":
            return response.get("Blocks", [])
        elif status in ("FAILED", "PARTIAL_SUCCESS"):
            raise RuntimeError(
                f"Textract job {job_id} failed with status: {status}. "
                f"StatusMessage: {response.get('StatusMessage', 'N/A')}"
            )

        time.sleep(2)

    raise TimeoutError(
        f"Textract job {job_id} did not complete within {max_wait} seconds."
    )


def _parse_textract_blocks(blocks: list, key: str) -> OCRResult:
    """Parse Textract block responses into a normalized OCRResult."""
    words = []
    total_confidence = 0.0
    word_count = 0
    page_count = 0

    for block in blocks:
        block_type = block.get("BlockType", "")

        if block_type == "LINE":
            text = block.get("Text", "")
            confidence = block.get("Confidence", 0.0)
            words.append({"text": text, "confidence": confidence, "type": "LINE"})
            total_confidence += confidence
            word_count += 1
        elif block_type == "PAGE":
            page_count += 1
        elif block_type == "WORD":
            text = block.get("Text", "")
            confidence = block.get("Confidence", 0.0)
            words.append({"text": text, "confidence": confidence, "type": "WORD"})
            total_confidence += confidence
            word_count += 1

    avg_confidence = (total_confidence / word_count) if word_count > 0 else 0.0

    extracted_text = " ".join(
        w["text"] for w in words if w.get("type") == "LINE"
    )

    return OCRResult(
        text=extracted_text,
        confidence=round(avg_confidence, 2),
        pages=max(page_count, 1),
        blocks=blocks,
    )
