import os

import boto3


def stored_asset_summary(text: str):
    bedrock = boto3.client(
        "bedrock-runtime",
        region_name=os.environ.get("AWS_REGION")
        or os.environ.get("AWS_DEFAULT_REGION"),
    )
    payload = {
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"Summarize this asset content concisely:\n{text}",
                    }
                ],
            }
        ],
        "max_tokens": 256,
        "anthropic_version": "bedrock-2023-05-31",
    }
    response = bedrock.converse(
        modelId=os.environ.get(
            "BEDROCK_MODEL_ID", "anthropic.claude-3-sonnet-20240229-v1:0"
        ),
        messages=payload["messages"],
        inferenceConfig={"maxTokens": 256},
    )
    return response
