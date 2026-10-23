import json
import boto3
import os
from typing import Optional, Dict, Any
from botocore.exceptions import ClientError
from storage_client import get_bedrock_client
from storage_models import SummaryResult


def summarize_text_with_titan(text: str, max_tokens: int = 500) -> SummaryResult:
    """
    Summarize text using Amazon Titan model via Bedrock.

    Args:
        text: Text to summarize
        max_tokens: Maximum tokens in summary (default: 500)

    Returns:
        SummaryResult with generated summary
    """
    bedrock_client = get_bedrock_client()

    # Titan Text G1 - Express model ID
    model_id = "amazon.titan-text-express-v1"

    try:
        # Prepare the prompt for summarization
        prompt = f"""Please provide a concise summary of the following text:

{text}

Summary:"""

        # Prepare request body for Titan model
        body = json.dumps(
            {
                "inputText": prompt,
                "textGenerationConfig": {
                    "maxTokenCount": max_tokens,
                    "temperature": 0.2,
                    "topP": 0.9,
                },
            }
        )

        # Invoke the model
        response = bedrock_client.invoke_model(
            modelId=model_id,
            body=body,
            contentType="application/json",
            accept="application/json",
        )

        # Parse the response
        response_body = json.loads(response["body"].read())

        if "results" in response_body and len(response_body["results"]) > 0:
            summary = response_body["results"][0]["outputText"].strip()
            return SummaryResult(success=True, summary=summary, model_id=model_id)
        else:
            return SummaryResult(
                success=False, error="No summary generated in response"
            )

    except ClientError as e:
        error_code = e.response["Error"]["Code"]
        error_msg = e.response["Error"]["Message"]
        return SummaryResult(
            success=False, error=f"Bedrock error ({error_code}): {error_msg}"
        )
    except Exception as e:
        return SummaryResult(success=False, error=f"Unexpected error: {str(e)}")


def summarize_document_from_s3(
    bucket_name: str, object_key: str, max_tokens: int = 500
) -> SummaryResult:
    """
    Summarize content extracted from a document stored in S3.

    Args:
        bucket_name: S3 bucket name containing the document
        object_key: S3 object key of the document
        max_tokens: Maximum tokens in summary (default: 500)

    Returns:
        SummaryResult with generated summary
    """
    # First extract text using OCR
    from stored_document_ocr import extract_text_from_s3_document

    ocr_result = extract_text_from_s3_document(bucket_name, object_key)

    if not ocr_result.success:
        return SummaryResult(success=False, error=f"OCR failed: {ocr_result.error}")

    if not ocr_result.text:
        return SummaryResult(success=False, error="No text extracted from document")

    # Summarize the extracted text
    return summarize_text_with_titan(ocr_result.text, max_tokens)


def summarize_with_custom_prompt(
    text: str,
    prompt_template: str,
    model_id: str = "amazon.titan-text-express-v1",
    max_tokens: int = 500,
) -> SummaryResult:
    """
    Summarize text with a custom prompt using specified Bedrock model.

    Args:
        text: Text to summarize
        prompt_template: Prompt template with {text} placeholder
        model_id: Bedrock model ID (default: Titan Text Express)
        max_tokens: Maximum tokens in response

    Returns:
        SummaryResult with generated summary
    """
    bedrock_client = get_bedrock_client()

    try:
        # Format the prompt
        prompt = prompt_template.format(text=text)

        # Prepare request body based on model
        if "titan" in model_id.lower():
            body = json.dumps(
                {
                    "inputText": prompt,
                    "textGenerationConfig": {
                        "maxTokenCount": max_tokens,
                        "temperature": 0.2,
                        "topP": 0.9,
                    },
                }
            )
        elif "claude" in model_id.lower():
            body = json.dumps(
                {
                    "prompt": f"\n\nHuman: {prompt}\n\nAssistant:",
                    "max_tokens_to_sample": max_tokens,
                    "temperature": 0.2,
                    "top_p": 0.9,
                }
            )
        else:
            # Generic Anthropic-style format
            body = json.dumps(
                {
                    "prompt": f"\n\nHuman: {prompt}\n\nAssistant:",
                    "max_tokens_to_sample": max_tokens,
                    "temperature": 0.2,
                    "top_p": 0.9,
                }
            )

        # Invoke the model
        response = bedrock_client.invoke_model(
            modelId=model_id,
            body=body,
            contentType="application/json",
            accept="application/json",
        )

        # Parse the response
        response_body = json.loads(response["body"].read())

        # Extract text based on model type
        if "titan" in model_id.lower():
            if "results" in response_body and len(response_body["results"]) > 0:
                summary = response_body["results"][0]["outputText"].strip()
            else:
                return SummaryResult(
                    success=False, error="No summary generated in response"
                )
        elif "claude" in model_id.lower():
            summary = response_body.get("completion", "").strip()
        else:
            # Try to extract from common response formats
            summary = response_body.get(
                "outputText", response_body.get("completion", "")
            ).strip()

        if summary:
            return SummaryResult(success=True, summary=summary, model_id=model_id)
        else:
            return SummaryResult(success=False, error="Empty summary generated")

    except ClientError as e:
        error_code = e.response["Error"]["Code"]
        error_msg = e.response["Error"]["Message"]
        return SummaryResult(
            success=False, error=f"Bedrock error ({error_code}): {error_msg}"
        )
    except Exception as e:
        return SummaryResult(success=False, error=f"Unexpected error: {str(e)}")
