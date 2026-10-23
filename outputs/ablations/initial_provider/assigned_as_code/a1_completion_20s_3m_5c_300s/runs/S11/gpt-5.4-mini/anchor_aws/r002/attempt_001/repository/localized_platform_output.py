import boto3


def localized_platform_output(payload, config=None):
    config = config or {}
    client = boto3.client("bedrock-runtime", region_name=config.get("region", "us-east-1"))
    response = client.converse(
        modelId=config.get("model_id", "us.amazon.nova-pro-v1:0"),
        messages=[
            {
                "role": "user",
                "content": [{"text": f'Translate the following text to {config.get("locale", "es-ES")}: {payload["text"]}'}],
            }
        ],
    )
    return {"text": response["output"]["message"]["content"][0].get("text", ""), "response": response}
