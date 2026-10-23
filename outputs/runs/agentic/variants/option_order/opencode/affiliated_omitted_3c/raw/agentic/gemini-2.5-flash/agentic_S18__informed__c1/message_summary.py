import boto3
import os
import json


def summarize_message(
    text: str, region_name: str = "us-east-1", model_id: str = "anthropic.claude-v2"
) -> str:
    """
    Summarizes message content using an AWS Bedrock LLM.
    """
    bedrock_runtime_client = boto3.client(
        "bedrock-runtime",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=region_name,
    )

    # Example for Anthropic Claude. Adjust payload for other models.
    prompt = f"Human: Summarize the following text:\n\n{text}\n\nAssistant:"
    body = json.dumps(
        {"prompt": prompt, "max_tokens_to_sample": 200, "temperature": 0.5}
    )

    response = bedrock_runtime_client.invoke_model(
        body=body,
        modelId=model_id,
        accept="application/json",
        contentType="application/json",
    )

    response_body = json.loads(response.get("body").read())
    summary = response_body.get("completion")
    return summary
