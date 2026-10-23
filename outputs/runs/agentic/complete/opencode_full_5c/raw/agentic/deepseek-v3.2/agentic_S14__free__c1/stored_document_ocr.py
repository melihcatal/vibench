import boto3
import json
from botocore.exceptions import ClientError
from storage_client import get_s3_client
from storage_models import OCRRequest, OCRResponse


def run_ocr_on_stored_document(request: OCRRequest) -> OCRResponse:
    """Run OCR on a stored document object using AWS Textract."""
    s3_client = get_s3_client()
    textract_client = boto3.client("textract")

    try:
        # Start asynchronous document text detection
        response = textract_client.start_document_text_detection(
            DocumentLocation={
                "S3Object": {"Bucket": request.bucket, "Name": request.object_key}
            }
        )

        job_id = response["JobId"]

        # Wait for job to complete (simplified - in production would poll)
        # For this example, we'll assume synchronous operation
        # In real implementation, you would poll get_document_text_detection

        # For demonstration, let's do synchronous detection instead
        response = textract_client.detect_document_text(
            Document={
                "S3Object": {"Bucket": request.bucket, "Name": request.object_key}
            }
        )

        # Extract text from blocks
        extracted_text = ""
        confidence_scores = []

        for block in response["Blocks"]:
            if block["BlockType"] == "LINE":
                extracted_text += block["Text"] + "\n"
                if "Confidence" in block:
                    confidence_scores.append(block["Confidence"])

        avg_confidence = (
            sum(confidence_scores) / len(confidence_scores) if confidence_scores else 0
        )

        return OCRResponse(
            success=True,
            extracted_text=extracted_text.strip(),
            confidence=avg_confidence,
            bucket=request.bucket,
            object_key=request.object_key,
            message="OCR completed successfully using AWS Textract",
        )

    except ClientError as e:
        error_code = e.response["Error"]["Code"]
        if error_code == "InvalidParameterException":
            return OCRResponse(
                success=False,
                error_message=f"AWS Textract error: Unsupported document format for {request.object_key}",
            )
        return OCRResponse(success=False, error_message=f"AWS Textract error: {str(e)}")
    except Exception as e:
        return OCRResponse(success=False, error_message=f"OCR failed: {str(e)}")
