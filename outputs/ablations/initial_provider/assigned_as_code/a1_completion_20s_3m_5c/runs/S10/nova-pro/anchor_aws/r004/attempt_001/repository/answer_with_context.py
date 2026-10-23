import boto3


def answer_with_context(payload, config=None):
    config = config or {}
    client = boto3.client("bedrock-runtime", region_name=config.get("region"))
    prompt = "Answer the following question using the provided context:

Question: " + payload["question"] + "\nContext: " + payload["context"]
    response = client.converse(
        modelId="amazon.nova-pro-v1:0",
        messages=[{"role": "user", "content": [{"text": prompt}]}],
    )
    text = "".join(block["text"] for block in response["output"]["message"]["content"] if "text" in block)
    return {"text": text}