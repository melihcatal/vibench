import boto3
import json
from botocore.exceptions import ClientError
from storage_client import get_s3_client
from storage_models import OCRRequest, OCRResponse
import base64


def run_stored_document_ocr(request: OCRRequest) -> OCRResponse:
    """
    Run OCR on a stored document object using AWS Textract.
    """
    # First, get the S3 client
    s3_client = get_s3_client()

    try:
        # Create Textract client for OCR
        textract_client = boto3.client("textract")

        # Call AWS Textract to detect text in the S3 document
        response = textract_client.detect_document_text(
            Document={"S3Object": {"Bucket": request.bucket, "Name": request.key}}
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
        avg_confidence = None
        if confidence_scores:
            avg_confidence = sum(confidence_scores) / len(confidence_scores)

        return OCRResponse(
            success=True,
            bucket=request.bucket,
            key=request.key,
            extracted_text=extracted_text.strip(),
            confidence=avg_confidence,
            message=f"OCR completed for s3://{request.bucket}/{request.key} using AWS Textract",
        )

    except ClientError as e:
        error_code = e.response["Error"]["Code"]
        if error_code == "InvalidS3ObjectException":
            return OCRResponse(
                success=False,
                bucket=request.bucket,
                key=request.key,
                error_message=f"AWS Textract error: Invalid S3 object - {str(e)}",
            )
        elif error_code == "UnsupportedDocumentException":
            return OCRResponse(
                success=False,
                bucket=request.bucket,
                key=request.key,
                error_message=f"AWS Textract error: Unsupported document format - {str(e)}",
            )
        else:
            return OCRResponse(
                success=False,
                bucket=request.bucket,
                key=request.key,
                error_message=f"AWS Textract error: {str(e)}",
            )
    except Exception as e:
        return OCRResponse(
            success=False,
            bucket=request.bucket,
            key=request.key,
            error_message=f"OCR processing error: {str(e)}",
        )
