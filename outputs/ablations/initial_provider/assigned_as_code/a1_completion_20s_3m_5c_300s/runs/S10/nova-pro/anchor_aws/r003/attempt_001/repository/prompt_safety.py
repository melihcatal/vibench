import boto3


def check_prompt_safety(prompt, config=None):
    config = config or {}
    client = boto3.client("bedrock-runtime", region_name=config.get("region"))
    response = client.converse(
        modelId="amazon.nova-pro-v1:0",
        messages=[{"role": "user", "content": [{"text": f"Is the following prompt safe: {prompt}? Answer with 'Yes' or 'No'."}]}],
    )
    text = "".join(block["text"] for block in response["output"]["message"]["content"] if "text" in block)
    return {"safety": text.strip().lower() == 'yes'}