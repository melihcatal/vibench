from safety_client import get_bedrock_runtime_client
from safety_models import normalize_texts


def moderation_summary(payload, config=None):
    config = config or {}
    client = get_bedrock_runtime_client(config)
    texts = normalize_texts(payload)
    prompt = "Summarize these moderation decisions for a human reviewer:\n" + "\n".join(texts)
    response = client.invoke_model(
        modelId=config.get("model_id", "anthropic.claude-3-haiku-20240307-v1:0"),
        body=("{" + f'"inputText": {prompt!r}' + "}").encode("utf-8"),
        contentType="application/json",
        accept="application/json",
    )
    return {"summary": response["body"].read().decode("utf-8")}
