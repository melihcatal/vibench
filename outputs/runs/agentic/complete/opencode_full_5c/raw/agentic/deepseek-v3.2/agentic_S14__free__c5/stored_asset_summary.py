import boto3
from botocore.exceptions import ClientError
import json
from storage_models import SummaryRequest, SummaryResponse


def summarize_stored_asset_content(request: SummaryRequest) -> SummaryResponse:
    """
    Summarize content extracted from a stored asset using AWS Bedrock with Anthropic Claude.
    """
    try:
        # Create Bedrock runtime client
        bedrock_client = boto3.client("bedrock-runtime")

        # Prepare prompt for Claude
        prompt = f"""Human: Please provide a concise summary of the following text. 
        The summary should be approximately {request.max_length} characters or less.
        
        Text to summarize:
        {request.text}
        
        Assistant:"""

        # Call AWS Bedrock with Claude model
        response = bedrock_client.invoke_model(
            modelId="anthropic.claude-v2",
            contentType="application/json",
            accept="application/json",
            body=json.dumps(
                {
                    "prompt": prompt,
                    "max_tokens_to_sample": 300,
                    "temperature": 0.5,
                    "top_p": 0.9,
                }
            ),
        )

        # Parse response
        response_body = json.loads(response["body"].read())
        summary = response_body.get("completion", "").strip()

        return SummaryResponse(
            success=True,
            original_text=request.text,
            summary=summary,
            message=f"Summary generated using AWS Bedrock with Anthropic Claude model",
        )

    except ClientError as e:
        error_code = e.response["Error"]["Code"]
        if error_code == "ValidationException":
            return SummaryResponse(
                success=False,
                original_text=request.text,
                error_message=f"AWS Bedrock error: Validation failed - {str(e)}",
            )
        elif error_code == "ModelErrorException":
            return SummaryResponse(
                success=False,
                original_text=request.text,
                error_message=f"AWS Bedrock error: Model error - {str(e)}",
            )
        else:
            return SummaryResponse(
                success=False,
                original_text=request.text,
                error_message=f"AWS Bedrock error: {str(e)}",
            )
    except Exception as e:
        return SummaryResponse(
            success=False,
            original_text=request.text,
            error_message=f"Summary generation error: {str(e)}",
        )
