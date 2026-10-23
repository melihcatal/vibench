from model_client import get_bedrock_client, get_model_id


def answer_with_context(payload, config=None):
    client = get_bedrock_client(config)
    prompt = "Answer the question using only the provided context.\n\nContext:\n" + payload["context"] + "\n\nQuestion:\n" + payload["question"]
    response = client.converse(
        modelId=get_model_id(config),
        messages=[{"role": "user", "content": [{"text": prompt}]}],
    )
    text = "".join(block["text"] for block in response["output"]["message"]["content"] if "text" in block)
    return {"text": text}
