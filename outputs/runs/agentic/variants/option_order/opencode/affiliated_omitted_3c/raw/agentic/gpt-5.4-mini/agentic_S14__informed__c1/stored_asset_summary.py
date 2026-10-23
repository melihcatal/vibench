import boto3


def stored_asset_summary(text, model_id="anthropic.claude-3-sonnet-20240229-v1:0"):
    client = boto3.client("bedrock-runtime")
    response = client.converse(
        modelId=model_id,
        messages=[
            {
                "role": "user",
                "content": [{"text": f"Summarize this asset concisely:\n{text}"}],
            }
        ],
    )
    return response["output"]["message"]["content"][0]["text"]
