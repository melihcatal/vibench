import boto3
import json
from botocore.exceptions import ClientError
import base64
from storage_client import get_s3_client
from storage_models import OCRRequest, OCRResponse


def run_ocr_on_stored_document(request: OCRRequest) -> OCRResponse:
    """Run OCR on a stored document object using AWS Textract."""
    s3_client = get_s3_client()

    try:
        # Initialize AWS Textract client
        textract_client = boto3.client(
            "textract",
            region_name="us-east-1",
            aws_access_key_id=boto3.Session().get_credentials().access_key,
            aws_secret_access_key=boto3.Session().get_credentials().secret_key,
        )

        # Call Textract for document text detection
        response = textract_client.detect_document_text(
            Document={
                "S3Object": {"Bucket": request.bucket, "Name": request.object_key}
            }
        )

        # Extract text from Textract response
        extracted_text = ""
        confidence_scores = []

        for block in response.get("Blocks", []):
            if block["BlockType"] == "LINE":
                extracted_text += block["Text"] + "\n"
                if "Confidence" in block:
                    confidence_scores.append(block["Confidence"])

        # Calculate average confidence
        avg_confidence = (
            sum(confidence_scores) / len(confidence_scores) if confidence_scores else 0
        )

        return OCRResponse(
            success=True,
            object_key=request.object_key,
            bucket=request.bucket,
            extracted_text=extracted_text.strip(),
            confidence=avg_confidence,
            message=f"Successfully extracted text from document using AWS Textract OCR",
        )

    except ClientError as e:
        error_code = e.response["Error"]["Code"] if "Error" in e.response else "Unknown"
        return OCRResponse(
            success=False,
            object_key=request.object_key,
            bucket=request.bucket,
            error_message=str(e),
            message=f"AWS Textract OCR failed: {error_code}",
        )
    except Exception as e:
        return OCRResponse(
            success=False,
            object_key=request.object_key,
            bucket=request.bucket,
            error_message=str(e),
            message=f"OCR processing failed: {str(e)}",
        )
