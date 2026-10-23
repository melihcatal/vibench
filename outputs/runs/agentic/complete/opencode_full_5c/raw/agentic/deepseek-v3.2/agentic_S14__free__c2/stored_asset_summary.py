import boto3
import json
from botocore.exceptions import ClientError
from storage_models import SummaryRequest, SummaryResponse


def summarize_extracted_content(request: SummaryRequest) -> SummaryResponse:
    """Summarize content extracted from a stored asset using AWS Bedrock."""

    try:
        # Initialize AWS Bedrock runtime client
        bedrock_client = boto3.client(
            "bedrock-runtime",
            region_name="us-east-1",
            aws_access_key_id=boto3.Session().get_credentials().access_key,
            aws_secret_access_key=boto3.Session().get_credentials().secret_key,
        )

        # Prepare prompt for summarization using Claude model
        prompt = f"""Human: Please summarize the following text in about {request.max_length} words:

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
                    "max_tokens_to_sample": 500,
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
            summary=summary,
            original_length=len(request.text),
            summary_length=len(summary),
            message=f"Successfully summarized content using AWS Bedrock Claude model",
        )

    except ClientError as e:
        error_code = e.response["Error"]["Code"] if "Error" in e.response else "Unknown"
        return SummaryResponse(
            success=False,
            error_message=str(e),
            message=f"AWS Bedrock summarization failed: {error_code}",
        )
    except Exception as e:
        return SummaryResponse(
            success=False,
            error_message=str(e),
            message=f"Summarization failed: {str(e)}",
        )
