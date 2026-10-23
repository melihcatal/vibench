import boto3
import json
import os
from typing import Dict, Any


def invoke_bedrock_model(
    model_id: str, prompt: str, max_tokens: int = 1000, temperature: float = 0.7
) -> Dict[str, Any]:
    """
    Invoke a provider-managed model through Amazon Bedrock.
    """
    bedrock_runtime = boto3.client(
        "bedrock-runtime",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_REGION", "us-east-1"),
    )

    if "anthropic" in model_id:
        body = json.dumps(
            {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": max_tokens,
                "temperature": temperature,
                "messages": [{"role": "user", "content": prompt}],
            }
        )
    elif "meta" in model_id:
        body = json.dumps(
            {"prompt": prompt, "max_gen_len": max_tokens, "temperature": temperature}
        )
    elif "amazon" in model_id:
        body = json.dumps(
            {
                "inputText": prompt,
                "textGenerationConfig": {
                    "maxTokenCount": max_tokens,
                    "temperature": temperature,
                },
            }
        )
    else:
        body = json.dumps(
            {"prompt": prompt, "max_tokens": max_tokens, "temperature": temperature}
        )

    response = bedrock_runtime.invoke_model(
        modelId=model_id,
        contentType="application/json",
        accept="application/json",
        body=body,
    )

    response_body = json.loads(response["body"].read())

    if "anthropic" in model_id:
        text = response_body["content"][0]["text"]
    elif "meta" in model_id:
        text = response_body["generation"]
    elif "amazon" in model_id:
        text = response_body["results"][0]["outputText"]
    else:
        text = response_body.get("completion", response_body.get("generated_text", ""))

    return {"text": text, "model_id": model_id, "response": response_body}
