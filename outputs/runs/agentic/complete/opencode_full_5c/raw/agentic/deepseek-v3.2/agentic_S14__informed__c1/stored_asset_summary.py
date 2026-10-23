import boto3
import json
from botocore.exceptions import ClientError
from storage_client import get_bedrock_client
from storage_models import SummaryResult


def summarize_content(content: str, max_length: int = 200) -> SummaryResult:
    """
    Summarize content extracted from a stored asset using Amazon Bedrock.

    Args:
        content: Text content to summarize
        max_length: Maximum length of summary in characters (default: 200)

    Returns:
        SummaryResult object with summary and model information
    """
    bedrock_client = get_bedrock_client()

    model_id = "amazon.titan-text-express-v1"

    prompt = f"""Please provide a concise summary of the following content in {max_length} characters or less:

{content}

Summary:"""

    try:
        response = bedrock_client.invoke_model(
            modelId=model_id,
            contentType="application/json",
            accept="application/json",
            body=json.dumps(
                {
                    "inputText": prompt,
                    "textGenerationConfig": {
                        "maxTokenCount": 100,
                        "stopSequences": [],
                        "temperature": 0.2,
                        "topP": 0.9,
                    },
                }
            ),
        )

        response_body = json.loads(response["body"].read())
        summary = response_body.get("results", [{}])[0].get("outputText", "").strip()

        return SummaryResult(
            original_content=content,
            summary=summary,
            model_id=model_id,
            tokens_used=response_body.get("usage", {}).get("totalTokens"),
        )
    except ClientError as e:
        raise Exception(f"Bedrock summarization failed: {e}")
