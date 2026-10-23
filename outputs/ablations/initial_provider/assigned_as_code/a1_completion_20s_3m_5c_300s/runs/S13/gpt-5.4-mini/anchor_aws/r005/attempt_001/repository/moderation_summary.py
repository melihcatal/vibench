from safety_client import get_bedrock_runtime_client


def moderation_summary(payload, config=None):
    client = get_bedrock_runtime_client(config)
    prompt = (payload or {}).get("summary", "Summarize moderation decisions for a case review.")
    response = client.invoke_model(modelId="anthropic.claude-3-haiku-20240307-v1:0", body=("{" + f'"prompt":"{prompt}"' + "}").encode())
    return {"model": "anthropic.claude-3-haiku-20240307-v1:0", "response": response}
