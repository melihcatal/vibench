import boto3
import json
from botocore.exceptions import ClientError
from storage_client import get_textract_client, get_s3_client
from storage_models import OCRResult


def extract_text_from_stored_document(bucket_name: str, document_key: str) -> OCRResult:
    """
    Run OCR on a stored document object using Amazon Textract.

    Args:
        bucket_name: S3 bucket name containing the document
        document_key: Object key (path) of the document in S3

    Returns:
        OCRResult object with extracted text and confidence
    """
    textract_client = get_textract_client()

    try:
        response = textract_client.detect_document_text(
            Document={"S3Object": {"Bucket": bucket_name, "Name": document_key}}
        )

        extracted_text = []
        confidence_sum = 0.0
        confidence_count = 0

        for block in response.get("Blocks", []):
            if block["BlockType"] == "LINE":
                extracted_text.append(block.get("Text", ""))
                if "Confidence" in block:
                    confidence_sum += block["Confidence"]
                    confidence_count += 1

        full_text = "\n".join(extracted_text)
        avg_confidence = (
            confidence_sum / confidence_count if confidence_count > 0 else 0.0
        )

        return OCRResult(
            text=full_text,
            confidence=avg_confidence,
            pages=1,  # Textract processes single pages by default
            raw_response=response,
        )
    except ClientError as e:
        raise Exception(f"Textract OCR failed: {e}")
