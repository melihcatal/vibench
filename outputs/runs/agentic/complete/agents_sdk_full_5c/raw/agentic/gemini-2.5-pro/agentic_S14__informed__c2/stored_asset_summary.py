import boto3
import json
import os


def summarize_text(text_content: str, max_tokens: int = 512) -> str:
    """
    Summarizes text content using an Anthropic Claude model via Amazon Bedrock.

    :param text_content: The text to be summarized.
    :param max_tokens: The maximum number of tokens for the summary.
    :return: The summarized text.
    """
    # Provider: Amazon Bedrock
    # Model Family: Anthropic Claude
    model_id = "anthropic.claude-3-sonnet-20240229-v1:0"

    bedrock_runtime_client = boto3.client(
        "bedrock-runtime", region_name=os.environ.get("AWS_REGION", "us-east-1")
    )

    prompt = f"\n\nHuman: Please provide a concise summary of the following text:\n\n<text>{text_content}</text>\n\nAssistant:"

    request_body = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": max_tokens,
        "messages": [
            {
                "role": "user",
                "content": [{"type": "text", "text": prompt}],
            }
        ],
    }

    try:
        response = bedrock_runtime_client.invoke_model(
            body=json.dumps(request_body),
            modelId=model_id,
            contentType="application/json",
            accept="application/json",
        )
        response_body = json.loads(response["body"].read())
        summary = response_body["content"][0]["text"]
        return summary.strip()

    except Exception as e:
        print(f"An error occurred during summarization: {e}")
        return "Error: Could not generate summary."
