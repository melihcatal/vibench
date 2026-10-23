# select_platform_resource.py
"""Resolve a provider‑specific model or deployment identifier before invocation.
This helper looks up a Bedrock deployment alias by name or returns a fallback model ID.
The concrete AWS Bedrock provider is used here.
"""

import os
from model_client import get_bedrock_client

def resolve_deployment(alias_or_arn: str) -> str:
    """Return the actual deployment ARN/identifier for the given alias or ARN.

    In a real workflow you would query the Bedrock API (e.g., describe_model)
    to fetch the current deployment ARN that matches the provided alias.
    For this example we simply echo the input if it looks like an ARN;
    otherwise we map a few hard‑coded aliases to known ARNs.
    """
    if alias_or_arn.startswith("arn:aws:bedrock:"):
        return alias_or_arn
    # Simple alias → ARN mapping for demo purposes
    alias_map = {
        "bedrock-chatbot": "arn:aws:bedrock:us-east-1:123456789012:model/chatbot-demo-v1",
        "bedrock-summary": "arn:aws:bedrock:us-east-1:123456789012:model/summarizer-v2",
    }
    return alias_map.get(alias_or_arn.lower(), alias_or_arn)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Resolve a Bedrock deployment identifier")
    parser.add_argument("alias_or_arn", help="Alias or ARN to resolve")
    args = parser.parse_args()
    print(resolve_deployment(args.alias_or_arn))
