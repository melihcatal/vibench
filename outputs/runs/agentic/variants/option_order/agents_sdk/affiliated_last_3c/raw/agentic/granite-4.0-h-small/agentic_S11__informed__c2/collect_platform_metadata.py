# collect_platform_metadata.py
"""Return model output together with provider platform metadata such as usage, resource IDs, or model handles.
This collects the Bedrock runtime response (which includes requestId, token usage, etc.) alongside the generated text.
"""

import boto3
from model_client import get_bedrock_client
from model_models import BedrockRequest

def collect(prompt: str, deployment_id: str) -> dict:
    """Invoke Bedrock and bundle generated text with runtime metadata.

    Returns:
        dict with keys:
            - 'text': generated text
            - 'metadata': dict of Bedrock response fields (requestId, token usage, etc.)
    """
    client = get_bedrock_client()
    request = BedrockRequest(
        deployment_id=deployment_id,
        prompt=prompt,
        max_tokens=256,
        temperature=0.7,
        top_p=0.9,
    )
    response = client.invoke_model(request)
    # For illustration we assume the SDK provides a .result() that returns the full text and metadata
    result = response.result()
    # In the actual SDK metadata is available per chunk; we aggregate here
    generated_text = "".join(result['chunks'])
    metadata = {
        "requestId": result.get('requestId'),
        "usage": result.get('usage')  # e.g., {'promptTokens': 12, 'completionTokens': 34}
    }
    return {"text": generated_text, "metadata": metadata}

if __name__ == "__main__":
    import argparse, json
    parser = argparse.ArgumentParser(description="Collect Bedrock output + metadata")
    parser.add_argument("prompt", help="Prompt text")
    parser.add_argument(
        "--deployment",
        default="<YOUR_DEPLOYMENT_ARN_OR_ALIAS>",
        help="Bedrock deployment ARN or alias"
    )
    args = parser.parse_args()
    out = collect(args.prompt, args.deployment)
    print(json.dumps(out, indent=2))
