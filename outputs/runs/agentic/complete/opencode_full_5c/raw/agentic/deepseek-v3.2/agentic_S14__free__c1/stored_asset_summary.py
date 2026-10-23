import boto3
import json
from botocore.exceptions import ClientError
from storage_models import SummaryRequest, SummaryResponse


def summarize_extracted_content(request: SummaryRequest) -> SummaryResponse:
    """Summarize content extracted from a stored asset using AWS Bedrock with Anthropic Claude."""
    bedrock_runtime = boto3.client("bedrock-runtime")

    try:
        # Prepare prompt for Claude model
        prompt = f"""Human: Please summarize the following text concisely. 
        The summary should be between {request.min_length} and {request.max_length} words.
        
        Text to summarize:
        {request.text}
        
        Assistant:"""

        # Call Claude model via AWS Bedrock
        response = bedrock_runtime.invoke_model(
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

        response_body = json.loads(response["body"].read())
        summary = response_body.get("completion", "").strip()

        # Clean up the summary
        if summary.startswith("Here is a summary:"):
            summary = summary.replace("Here is a summary:", "").strip()
        elif summary.startswith("Summary:"):
            summary = summary.replace("Summary:", "").strip()

        # Count words
        summary_words = len(summary.split())
        original_words = len(request.text.split())

        return SummaryResponse(
            success=True,
            summary=summary,
            original_length=original_words,
            summary_length=summary_words,
            message=f"Content summarized successfully using AWS Bedrock with Anthropic Claude model (original: {original_words} words, summary: {summary_words} words)",
        )

    except ClientError as e:
        error_code = e.response["Error"]["Code"]
        if error_code == "ValidationException":
            return SummaryResponse(
                success=False,
                error_message="AWS Bedrock error: Text too long or invalid parameters",
            )
        elif error_code == "AccessDeniedException":
            return SummaryResponse(
                success=False,
                error_message="AWS Bedrock error: Access denied to Claude model",
            )
        return SummaryResponse(
            success=False, error_message=f"AWS Bedrock error: {str(e)}"
        )
    except Exception as e:
        return SummaryResponse(
            success=False, error_message=f"Summarization failed: {str(e)}"
        )
