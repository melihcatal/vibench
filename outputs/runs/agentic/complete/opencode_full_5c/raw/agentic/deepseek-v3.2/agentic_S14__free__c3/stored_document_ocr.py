import boto3
import os
from typing import Optional
from storage_client import get_s3_client
from storage_models import OCRRequest, OCRResponse
import tempfile


def run_stored_document_ocr(request: OCRRequest) -> OCRResponse:
    """
    Run OCR on a stored document object using AWS Textract.
    """
    try:
        # Download the document from S3
        s3_client = get_s3_client()

        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as temp_file:
            s3_client.download_file(
                Bucket=request.bucket, Key=request.object_key, Filename=temp_file.name
            )
            temp_path = temp_file.name

        # Initialize AWS Textract client
        textract_client = boto3.client(
            "textract",
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            region_name=os.getenv("AWS_REGION", "us-east-1"),
        )

        # Read the file content
        with open(temp_path, "rb") as document:
            image_bytes = document.read()

        # Call AWS Textract for OCR
        response = textract_client.detect_document_text(Document={"Bytes": image_bytes})

        # Extract text from response
        extracted_text = ""
        confidence_scores = []

        for item in response.get("Blocks", []):
            if item["BlockType"] == "LINE":
                extracted_text += item["Text"] + "\n"
                if "Confidence" in item:
                    confidence_scores.append(item["Confidence"])

        # Calculate average confidence
        avg_confidence = (
            sum(confidence_scores) / len(confidence_scores) if confidence_scores else 0
        )

        # Clean up temp file
        os.unlink(temp_path)

        return OCRResponse(
            success=True,
            extracted_text=extracted_text.strip(),
            confidence=avg_confidence,
            object_key=request.object_key,
            bucket=request.bucket,
            message=f"OCR completed for s3://{request.bucket}/{request.object_key} using AWS Textract",
        )

    except Exception as e:
        # Clean up temp file if it exists
        if "temp_path" in locals() and os.path.exists(temp_path):
            try:
                os.unlink(temp_path)
            except:
                pass

        return OCRResponse(
            success=False,
            object_key=request.object_key,
            bucket=request.bucket,
            error_message=str(e),
            message=f"OCR failed using AWS Textract: {e}",
        )
