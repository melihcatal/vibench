import os
import boto3
import json
from typing import Dict, Any

def summarize_stored_asset_content(
    text_content: str,
    max_tokens: int = 500,
    model_id: str = "anthropic.claude-3-sonnet-20240229-v1:0"
) -> str:
    """
    Summarizes content extracted from a stored asset using an LLM via Amazon Bedrock.
    Uses Anthropic Claude models (e.g., Claude 3 Sonnet).

    Args:
        text_content: The text content to summarize.
        max_tokens: The maximum number of tokens for the summary.
        model_id: The specific model ID to use (e.g., "anthropic.claude-3-sonnet-20240229-v1:0").

    Returns:
        The summarized text.
    """
    bedrock_runtime_client = boto3.client(
        'bedrock-runtime',
        region_name=os.getenv('AWS_REGION', 'us-east-1')
    )

    prompt = f"Human: Summarize the following text:
\n<text>\n{text_content}\n</text>\n\nAssistant:"

    body = json.dumps({
        "prompt": prompt,
        "max_tokens_to_sample": max_tokens,
        "temperature": 0.1,
        "top_p": 0.9
    })

    try:
        response = bedrock_runtime_client.invoke_model(
            body=body,
            modelId=model_id,
            accept='application/json',
            contentType='application/json'
        )

        response_body = json.loads(response.get('body').read())
        return response_body.get('completion')
    except Exception as e:
        print(f"Error summarizing text with Amazon Bedrock (Anthropic Claude): {e}")
        raise
