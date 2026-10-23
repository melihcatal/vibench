import boto3
import os
import json
from botocore.exceptions import ClientError
from storage_client import get_s3_client
from storage_models import OCRResult


def run_ocr_on_stored_document(bucket_name, object_key, feature_types=None):
    """
    Run OCR on a stored document object using Amazon Textract.

    Args:
        bucket_name: S3 bucket name containing the document
        object_key: S3 object key of the document
        feature_types: List of Textract features (default: ['TABLES', 'FORMS'])

    Returns:
        dict: OCR results or error
    """
    if feature_types is None:
        feature_types = ["TABLES", "FORMS"]

    textract_client = boto3.client("textract")

    try:
        # Start asynchronous document analysis
        response = textract_client.start_document_analysis(
            DocumentLocation={"S3Object": {"Bucket": bucket_name, "Name": object_key}},
            FeatureTypes=feature_types,
        )

        job_id = response["JobId"]

        # Wait for job to complete
        import time

        status = "IN_PROGRESS"
        while status == "IN_PROGRESS":
            time.sleep(2)
            response = textract_client.get_document_analysis(JobId=job_id)
            status = response["JobStatus"]

        if status == "SUCCEEDED":
            # Extract text from blocks
            blocks = response.get("Blocks", [])
            text_lines = []
            confidence_scores = []

            for block in blocks:
                if block["BlockType"] == "LINE":
                    text_lines.append(block.get("Text", ""))
                    confidence_scores.append(block.get("Confidence", 0))

            full_text = "\n".join(text_lines)
            avg_confidence = (
                sum(confidence_scores) / len(confidence_scores)
                if confidence_scores
                else 0
            )

            # Extract page information
            pages = []
            page_blocks = {}
            for block in blocks:
                page_index = block.get("Page", 1)
                if page_index not in page_blocks:
                    page_blocks[page_index] = []
                page_blocks[page_index].append(block)

            for page_num, page_blocks_list in page_blocks.items():
                page_text = "\n".join(
                    [
                        block.get("Text", "")
                        for block in page_blocks_list
                        if block["BlockType"] == "LINE"
                    ]
                )
                pages.append(
                    {
                        "page_number": page_num,
                        "text": page_text,
                        "block_count": len(page_blocks_list),
                    }
                )

            return {
                "success": True,
                "text": full_text,
                "confidence": avg_confidence,
                "pages": pages,
                "total_pages": len(pages),
                "job_id": job_id,
                "provider": "Amazon Textract",
                "model": "textract-document-analysis",
            }
        else:
            return {
                "success": False,
                "error": f"Textract job failed with status: {status}",
                "job_id": job_id,
                "provider": "Amazon Textract",
            }

    except ClientError as e:
        return {"success": False, "error": str(e), "provider": "Amazon Textract"}
    except Exception as e:
        return {"success": False, "error": str(e), "provider": "Amazon Textract"}
