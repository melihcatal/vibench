import os
from model_client import get_bedrock_client
from model_models import BedrockConverseResponse


def answer_with_context(payload, config=None):
    config = config or {}
    client = get_bedrock_client()
    
    context = payload["context"]
    question = payload["question"]

    prompt = (
        f"Context: {context}\n\n"
        f"Question: {question}\n\n"
        "Answer the question based solely on the provided context."
    )

    response = client.converse(
        modelId=os.environ.get("BEDROCK_MODEL_ID", "anthropic.claude-3-sonnet-20240229-v1:0"),
        messages=[{"role": "user", "content": [{"text": prompt}]}],
        inferenceConfig={
            "maxTokens": config.get("max_tokens", 500),
            "temperature": config.get("temperature", 0.1),
        },
    )
    
    text = "".join(block["text"] for block in response["output"]["message"]["content"] if "text" in block)
    return {"answer": text}
