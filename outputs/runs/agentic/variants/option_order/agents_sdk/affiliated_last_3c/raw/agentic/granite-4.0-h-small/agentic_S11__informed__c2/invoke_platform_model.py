# invoke_platform_model.py
"""Invoke a provider‑managed generative model via a concrete SDK client.
This example uses Amazon Bedrock (AWS) as the concrete provider.
It locates a deployment (or model) using select_platform_resource,
instantiates the Bedrock runtime client, and streams the model response.
"""

import os
import json
import boto3
from model_client import get_bedrock_client
from model_models import BedrockRequest, BedrockResponse

def infer(text: str, deployment_id: str) -> None:
    """Call the selected Bedrock deployment and stream output.

    Args:
        text: Prompt to send to the model.
        deployment_id: Bedrock deployment ARN or alias.
    """
    client = get_bedrock_client()
    request = BedrockRequest(
        deployment_id=deployment_id,
        prompt=text,
        max_tokens=256,
        temperature=0.7,
        top_p=0.9,
    )
    response = client.invoke_model(request)
    # Stream generation and emit response objects as they arrive
    for chunk in response.stream():
        print(chunk, end="", flush=True)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Invoke Amazon Bedrock generative model")
    parser.add_argument("prompt", help="Prompt text to send")
    parser.add_argument(
        "--deployment",
        default="<YOUR_DEPLOYMENT_ARN_OR_ALIAS>",
        help="Bedrock deployment ARN or alias"
    )
    args = parser.parse_args()
    infer(args.prompt, args.deployment)
