import boto3
import json
import os
from botocore.exceptions import ClientError
from storage_models import SummaryResult


def summarize_content_from_asset(
    text, model_id="anthropic.claude-3-sonnet-20240229-v1:0", max_tokens=500
):
    """
    Summarize content extracted from a stored asset using Amazon Bedrock.

    Args:
        text: Text content to summarize
        model_id: Bedrock model ID (default: Claude 3 Sonnet)
        max_tokens: Maximum tokens for summary

    Returns:
        dict: Summary results or error
    """
    bedrock_runtime = boto3.client("bedrock-runtime")

    try:
        # Prepare prompt for summarization
        prompt = f"""Human: Please provide a concise summary of the following text. Focus on the main points and key information.

Text to summarize:
{text[:4000]}  # Limit text length for API

Assistant:"""

        # Prepare request body for Claude model
        if "claude" in model_id.lower():
            body = json.dumps(
                {
                    "anthropic_version": "bedrock-2023-05-31",
                    "max_tokens": max_tokens,
                    "messages": [{"role": "user", "content": prompt}],
                }
            )
        else:
            # Generic format for other models
            body = json.dumps(
                {"prompt": prompt, "max_tokens": max_tokens, "temperature": 0.1}
            )

        # Invoke model
        response = bedrock_runtime.invoke_model(
            modelId=model_id,
            contentType="application/json",
            accept="application/json",
            body=body,
        )

        # Parse response
        response_body = json.loads(response["body"].read())

        if "claude" in model_id.lower():
            summary = response_body["content"][0]["text"]
        elif "titan" in model_id.lower():
            summary = response_body.get("results", [{}])[0].get("outputText", "")
        else:
            summary = response_body.get("generations", [{}])[0].get("text", "")

        # Estimate token count (rough approximation)
        token_count = len(summary.split())

        return {
            "success": True,
            "original_text_length": len(text),
            "summary": summary.strip(),
            "summary_length": len(summary),
            "token_count": token_count,
            "model_id": model_id,
            "provider": "Amazon Bedrock",
        }

    except ClientError as e:
        return {"success": False, "error": str(e), "provider": "Amazon Bedrock"}
    except Exception as e:
        return {"success": False, "error": str(e), "provider": "Amazon Bedrock"}


def summarize_stored_asset(
    bucket_name, object_key, model_id="anthropic.claude-3-sonnet-20240229-v1:0"
):
    """
    Extract text from stored asset and generate a summary.

    Args:
        bucket_name: S3 bucket name
        object_key: S3 object key
        model_id: Bedrock model ID

    Returns:
        dict: Combined extraction and summary results
    """
    # First extract text (try OCR for documents, otherwise read as text)
    from stored_document_ocr import run_ocr_on_stored_document

    # Check file extension to determine approach
    file_ext = os.path.splitext(object_key)[1].lower()

    if file_ext in [".pdf", ".jpg", ".jpeg", ".png", ".tiff", ".tif"]:
        # Use OCR for images/PDFs
        extraction_result = run_ocr_on_stored_document(bucket_name, object_key)
        if not extraction_result.get("success"):
            return {
                "success": False,
                "error": f"Text extraction failed: {extraction_result.get('error')}",
                "provider": "Amazon Bedrock + Textract",
            }
        extracted_text = extraction_result.get("text", "")
        extraction_method = "OCR (Textract)"
    else:
        # Try to read as text file
        try:
            from storage_client import get_s3_client

            s3_client = get_s3_client()
            response = s3_client.get_object(Bucket=bucket_name, Key=object_key)
            extracted_text = response["Body"].read().decode("utf-8", errors="ignore")
            extraction_method = "Direct text read"
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to read file as text: {str(e)}",
                "provider": "Amazon Bedrock",
            }

    if not extracted_text or len(extracted_text.strip()) < 10:
        return {
            "success": False,
            "error": "No meaningful text extracted from asset",
            "extraction_method": extraction_method,
            "provider": "Amazon Bedrock",
        }

    # Generate summary
    summary_result = summarize_content_from_asset(extracted_text, model_id)

    if summary_result.get("success"):
        return {
            "success": True,
            "extraction_method": extraction_method,
            "original_text_sample": extracted_text[:500] + "..."
            if len(extracted_text) > 500
            else extracted_text,
            "original_length": len(extracted_text),
            "summary": summary_result.get("summary"),
            "summary_length": summary_result.get("summary_length"),
            "model_id": model_id,
            "provider": "Amazon Bedrock",
        }
    else:
        return {
            "success": False,
            "error": f"Summary generation failed: {summary_result.get('error')}",
            "extraction_success": True,
            "extracted_text_sample": extracted_text[:500],
            "extraction_method": extraction_method,
            "provider": "Amazon Bedrock",
        }
