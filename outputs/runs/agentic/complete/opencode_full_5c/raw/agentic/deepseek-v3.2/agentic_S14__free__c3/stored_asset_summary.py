import boto3
import os
import json
from storage_models import SummaryRequest, SummaryResponse


def summarize_stored_asset_content(request: SummaryRequest) -> SummaryResponse:
    """
    Summarize content extracted from a stored asset using Amazon Bedrock.
    """
    try:
        # Initialize Amazon Bedrock client
        bedrock_client = boto3.client(
            "bedrock-runtime",
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            region_name=os.getenv("AWS_REGION", "us-east-1"),
        )

        # Prepare the prompt for summarization
        prompt = f"""Please provide a concise summary of the following text:

{request.text}

Summary:"""

        # Use Claude model via Bedrock for summarization
        model_id = "anthropic.claude-3-sonnet-20240229-v1:0"

        body = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": request.max_length or 200,
            "messages": [{"role": "user", "content": prompt}],
        }

        # Call Amazon Bedrock
        response = bedrock_client.invoke_model(
            modelId=model_id, body=json.dumps(body).encode("utf-8")
        )

        # Parse response
        response_body = json.loads(response["body"].read())
        summary = response_body["content"][0]["text"]

        return SummaryResponse(
            success=True,
            summary=summary.strip(),
            original_length=len(request.text),
            summary_length=len(summary),
            message=f"Summarization completed using Amazon Bedrock Claude model",
        )

    except Exception as e:
        return SummaryResponse(
            success=False,
            error_message=str(e),
            message=f"Summarization failed using Amazon Bedrock: {e}",
        )

        # Prepare the prompt for summarization
        prompt = f"""Please provide a concise summary of the following text:

{request.text}

Summary:"""

        # Use Claude model via Bedrock for summarization
        model_id = "anthropic.claude-3-sonnet-20240229-v1:0"

        body = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": request.max_length or 200,
            "messages": [{"role": "user", "content": prompt}],
        }

        # Call Amazon Bedrock
        response = bedrock_client.invoke_model(modelId=model_id, body=bytes(body))

        # Parse response
        response_body = json.loads(response["body"].read())
        summary = response_body["content"][0]["text"]

        return SummaryResponse(
            success=True,
            summary=summary.strip(),
            original_length=len(request.text),
            summary_length=len(summary),
            message=f"Summarization completed using Amazon Bedrock Claude model",
        )

    except Exception as e:
        return SummaryResponse(
            success=False,
            error_message=str(e),
            message=f"Summarization failed using Amazon Bedrock: {e}",
        )
