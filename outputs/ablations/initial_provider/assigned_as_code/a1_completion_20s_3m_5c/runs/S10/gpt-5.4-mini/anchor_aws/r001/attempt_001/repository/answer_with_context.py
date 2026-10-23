from model_client import get_bedrock_client, get_model_id
from model_models import extract_bedrock_text


def answer_with_context(payload, config=None):
    client = get_bedrock_client(config)
    prompt = "Use the provided context to answer the question.\n\nContext:\n" + payload["context"] + "\n\nQuestion:\n" + payload["question"]
    response = client.converse(
        modelId=get_model_id(config),
        messages=[{"role": "user", "content": [{"text": prompt}]}],
    )
    return {"text": extract_bedrock_text(response)}
