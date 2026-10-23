import boto3


def answer_with_context(payload, config=None):
    config = config or {}
    client = boto3.client("bedrock-runtime", region_name=config.get("region"))
    context = payload["context"]
    question = payload["question"]
    prompt = f"Using the following context, answer the question:\n\nContext: {context}\n\nQuestion: {question}"
    response = client.converse(
        modelId="amazon.nova-pro-v1:0",
        messages=[{"role": "user", "content": [{"text": prompt}]}],
        inferenceConfig={"maxTokens": 1024},
    )
    text = "".join(block["text"] for block in response["output"]["message"]["content"] if "text" in block)
    return {"answer": text}
