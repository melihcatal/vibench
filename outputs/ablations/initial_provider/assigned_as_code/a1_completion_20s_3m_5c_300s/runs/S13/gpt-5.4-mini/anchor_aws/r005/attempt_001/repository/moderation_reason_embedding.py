from safety_client import get_bedrock_runtime_client


def moderation_reason_embedding(payload, config=None):
    client = get_bedrock_runtime_client(config)
    text = (payload or {}).get("text", "")
    response = client.invoke_model(modelId="amazon.titan-embed-text-v2:0", body=("{" + f'"inputText":"{text}"' + "}").encode())
    return {"model": "amazon.titan-embed-text-v2:0", "response": response}
