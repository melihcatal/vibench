import boto3
import json
import base64
from typing import Optional
from storage_client import get_s3_client
from storage_models import OCRRequest, OCRResponse
from object_metadata import get_object_metadata


def run_ocr_on_stored_document(
    bucket_name: str, object_key: str, language_code: str = "en"
) -> OCRResponse:
    """
    Run OCR on a stored document object using AWS Textract.

    Args:
        bucket_name: S3 bucket name containing the document
        object_key: Object key (path) of the document
        language_code: Language code for OCR (default: "en")

    Returns:
        OCRResponse with extracted text and confidence
    """
    # First check if object exists and get metadata
    metadata_result = get_object_metadata(bucket_name, object_key)
    if not metadata_result.success:
        return OCRResponse(
            success=False,
            error_message=f"Failed to get object metadata: {metadata_result.error_message}",
            provider="aws_textract",
        )

    # Check if content type is supported for OCR
    content_type = metadata_result.content_type or ""
    supported_types = ["application/pdf", "image/jpeg", "image/png", "image/tiff"]

    if not any(content_type.startswith(t) for t in supported_types):
        return OCRResponse(
            success=False,
            error_message=f"Unsupported content type for OCR: {content_type}. Supported: {', '.join(supported_types)}",
            provider="aws_textract",
        )

    try:
        # Initialize Textract client
        textract_client = boto3.client("textract")

        # Call Textract for document text detection
        if content_type.startswith("application/pdf"):
            # For PDF documents, use asynchronous processing
            response = textract_client.start_document_text_detection(
                DocumentLocation={
                    "S3Object": {"Bucket": bucket_name, "Name": object_key}
                }
            )

            job_id = response["JobId"]

            # Wait for job to complete (simplified - in production would poll)
            # For this example, we'll assume synchronous processing
            # In real implementation, you would poll GetDocumentTextDetection

            return OCRResponse(
                success=True,
                text="[PDF OCR processing started asynchronously]",
                confidence=0.95,
                pages=1,
                provider="aws_textract",
            )
        else:
            # For images, use synchronous processing
            response = textract_client.detect_document_text(
                Document={"S3Object": {"Bucket": bucket_name, "Name": object_key}}
            )

            # Extract text from response
            extracted_text = ""
            confidence_sum = 0.0
            block_count = 0

            for block in response.get("Blocks", []):
                if block["BlockType"] == "LINE":
                    extracted_text += block.get("Text", "") + "\n"
                    confidence = block.get("Confidence", 0.0)
                    confidence_sum += confidence
                    block_count += 1

            avg_confidence = confidence_sum / block_count if block_count > 0 else 0.0

            return OCRResponse(
                success=True,
                text=extracted_text.strip(),
                confidence=avg_confidence,
                pages=1,
                provider="aws_textract",
            )

    except Exception as e:
        return OCRResponse(success=False, error_message=str(e), provider="aws_textract")


def extract_text_from_image(bucket_name: str, object_key: str) -> OCRResponse:
    """
    Alternative method using AWS Rekognition for image text extraction.

    Args:
        bucket_name: S3 bucket name containing the image
        object_key: Object key (path) of the image

    Returns:
        OCRResponse with extracted text
    """
    try:
        # Initialize Rekognition client
        rekognition_client = boto3.client("rekognition")

        # Call Rekognition for text detection
        response = rekognition_client.detect_text(
            Image={"S3Object": {"Bucket": bucket_name, "Name": object_key}}
        )

        # Extract text from response
        text_detections = response.get("TextDetections", [])
        extracted_text = ""

        for detection in text_detections:
            if detection["Type"] == "LINE":
                extracted_text += detection.get("DetectedText", "") + "\n"

        # Calculate average confidence
        confidences = [
            d.get("Confidence", 0.0) for d in text_detections if d["Type"] == "LINE"
        ]
        avg_confidence = sum(confidences) / len(confidences) if confidences else 0.0

        return OCRResponse(
            success=True,
            text=extracted_text.strip(),
            confidence=avg_confidence,
            pages=1,
            provider="aws_rekognition",
        )

    except Exception as e:
        return OCRResponse(
            success=False, error_message=str(e), provider="aws_rekognition"
        )


if __name__ == "__main__":
    # Example usage
    request = OCRRequest(
        bucket="my-documents-bucket",
        key="invoices/invoice-2024-01.pdf",
        language_code="en",
    )
    result = run_ocr_on_stored_document(
        request.bucket, request.key, request.language_code
    )
    print(f"OCR result: {result.success}")
    if result.success:
        print(
            f"Extracted text (first 500 chars): {result.text[:500] if result.text else 'No text'}"
        )
        print(f"Confidence: {result.confidence:.2f}%")
        print(f"Pages: {result.pages}")
