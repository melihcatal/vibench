import boto3
import os
import json
from botocore.exceptions import ClientError


def summarize_content_from_asset(
    text: str, bedrock_client=None, model_id: str = "amazon.titan-text-express-v1"
) -> dict:
    """
    Summarize content extracted from a stored asset using Amazon Bedrock (Titan model).

    Args:
        text: Text content to summarize
        bedrock_client: Optional Bedrock Runtime client (will create if not provided)
        model_id: Bedrock model ID (default: 'amazon.titan-text-express-v1')

    Returns:
        Dictionary with summarization results
    """
    # Create Bedrock Runtime client if not provided
    if bedrock_client is None:
        aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
        aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
        aws_region = os.getenv("AWS_REGION", "us-east-1")

        if not aws_access_key_id or not aws_secret_access_key:
            raise ValueError(
                "AWS credentials not found in environment. "
                "Please set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY."
            )

        bedrock_client = boto3.client(
            "bedrock-runtime",
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=aws_region,
        )

    try:
        # Prepare prompt for summarization
        prompt = f"""Please provide a concise summary of the following text:

{text}

Summary:"""

        # Prepare request body for Titan model
        body = json.dumps(
            {
                "inputText": prompt,
                "textGenerationConfig": {
                    "maxTokenCount": 500,
                    "stopSequences": [],
                    "temperature": 0.1,
                    "topP": 0.9,
                },
            }
        )

        # Call Amazon Bedrock
        response = bedrock_client.invoke_model(
            body=body,
            modelId=model_id,
            accept="application/json",
            contentType="application/json",
        )

        # Parse response
        response_body = json.loads(response["body"].read())

        # Extract generated text
        generated_text = (
            response_body.get("results", [{}])[0].get("outputText", "").strip()
        )

        # Extract token counts
        input_token_count = response_body.get("inputTextTokenCount", 0)
        output_token_count = len(
            response_body.get("results", [{}])[0].get("tokenCount", [])
        )

        return {
            "success": True,
            "original_text_length": len(text),
            "summary": generated_text,
            "summary_length": len(generated_text),
            "model_id": model_id,
            "input_token_count": input_token_count,
            "output_token_count": output_token_count,
            "compression_ratio": len(generated_text) / max(len(text), 1),
        }

    except ClientError as e:
        error_code = e.response.get("Error", {}).get("Code", "Unknown")
        return {
            "success": False,
            "error": str(e),
            "error_code": error_code,
            "model_id": model_id,
            "original_text_length": len(text),
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "model_id": model_id,
            "original_text_length": len(text),
        }


def summarize_asset_from_ocr(
    ocr_result: dict, model_id: str = "amazon.titan-text-express-v1"
) -> dict:
    """
    Summarize content from OCR results.

    Args:
        ocr_result: OCR result dictionary from stored_document_ocr.py
        model_id: Bedrock model ID (default: 'amazon.titan-text-express-v1')

    Returns:
        Dictionary with summarized OCR results
    """
    if not ocr_result.get("success", False):
        return {
            "success": False,
            "error": "OCR result was not successful",
            "ocr_result": ocr_result,
        }

    full_text = ocr_result.get("full_text", "")
    if not full_text:
        return {
            "success": False,
            "error": "No text found in OCR results",
            "ocr_result": ocr_result,
        }

    # Summarize the text
    summary_result = summarize_content_from_asset(text=full_text, model_id=model_id)

    if not summary_result.get("success", False):
        return summary_result

    # Return combined result
    return {
        "success": True,
        "ocr_result": ocr_result,
        "summary_result": summary_result,
        "bucket": ocr_result.get("bucket", ""),
        "key": ocr_result.get("key", ""),
        "original_text_length": len(full_text),
        "summary": summary_result.get("summary", ""),
        "summary_length": summary_result.get("summary_length", 0),
        "model_id": model_id,
        "compression_ratio": summary_result.get("compression_ratio", 0),
    }


def summarize_translated_text(
    translation_result: dict, model_id: str = "amazon.titan-text-express-v1"
) -> dict:
    """
    Summarize translated text.

    Args:
        translation_result: Translation result dictionary from stored_text_translate.py
        model_id: Bedrock model ID (default: 'amazon.titan-text-express-v1')

    Returns:
        Dictionary with summarized translation results
    """
    if not translation_result.get("success", False):
        return {
            "success": False,
            "error": "Translation result was not successful",
            "translation_result": translation_result,
        }

    translated_text = translation_result.get("translated_text", "")
    if not translated_text:
        return {
            "success": False,
            "error": "No translated text found",
            "translation_result": translation_result,
        }

    # Summarize the translated text
    summary_result = summarize_content_from_asset(
        text=translated_text, model_id=model_id
    )

    if not summary_result.get("success", False):
        return summary_result

    # Return combined result
    return {
        "success": True,
        "translation_result": translation_result,
        "summary_result": summary_result,
        "original_text": translation_result.get("original_text", ""),
        "translated_text": translated_text,
        "summary": summary_result.get("summary", ""),
        "summary_length": summary_result.get("summary_length", 0),
        "model_id": model_id,
        "source_language": translation_result.get("source_language", ""),
        "target_language": translation_result.get("target_language", ""),
    }
