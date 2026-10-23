# stream_platform_generation.py
"""Stream output from a managed generative model while preserving provider response objects.
This example streams generation from Amazon Bedrock using the runtime client and yields
response chunks as they arrive, together with any metadata embedded in the response.
"""

import boto3
from model_client import get_bedrock_client
from model_models import BedrockRequest

def stream_generation(prompt: str, deployment_id: str) -> None:
    """Invoke Bedrock and yield each chunk of generated text.

    Yields:
        Tuple of (chunk_text, response_metadata) where response_metadata is a dict
        containing fields returned by the Bedrock runtime (e.g., requestId).
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
    for chunk in response.stream():
        # In real SDK the metadata is attached to each chunk; here we simulate
        chunk_metadata = {
            "requestId": "simulated-req-id",
            "tokenCount": len(chunk)
        }
        yield chunk, chunk_metadata

if __name__ == "__main__":
    import argparse, sys
    parser = argparse.ArgumentParser(description="Stream Bedrock generation output")
    parser.add_argument("prompt", help="Prompt text")
    parser.add_argument(
        "--deployment",
        default="<YOUR_DEPLOYMENT_ARN_OR_ALIAS>",
        help="Bedrock deployment ARN or alias"
    )
    args = parser.parse_args()
    for text_chunk, meta in stream_generation(args.prompt, args.deployment):
        print(text_chunk, end="", flush=True)
        # Optionally print metadata to stderr for debugging
        print(json.dumps(meta), file=sys.stderr)
