import boto3


def platform_output_safety(payload, config=None):
    config = config or {}
    client = boto3.client("bedrock-runtime", region_name=config.get("region", "us-east-1"))
    response = client.converse(
        modelId=config.get("model_id", "us.amazon.nova-pro-v1:0"),
        messages=[{"role": "user", "content": [{"text": payload["text"]}]}],
        system=[{"text": "Assess the content for unsafe material and respond with a short safety verdict."}],
    )
    return {"verdict": response["output"]["message"]["content"][0].get("text", ""), "response": response}
