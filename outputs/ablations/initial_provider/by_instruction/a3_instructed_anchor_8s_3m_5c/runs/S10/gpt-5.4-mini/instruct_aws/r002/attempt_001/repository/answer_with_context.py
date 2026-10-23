import json
import os

from model_client import bedrock_runtime_client, model_id_for_task
from model_models import ChatRequest, normalize_text


def answer_with_context(context: str, question: str) -> str:
    request = ChatRequest(
        system="Answer the question using only the provided context.",
        user=f"Context:\n{context}\n\nQuestion:\n{question}",
        max_tokens=int(os.getenv("QA_MAX_TOKENS", "256")),
        temperature=float(os.getenv("QA_TEMPERATURE", "0.2")),
    )
    client = bedrock_runtime_client()
    response = client.invoke_model(
        modelId=model_id_for_task("answer"),
        body=json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": request.max_tokens,
            "temperature": request.temperature,
            "system": request.system,
            "messages": [{"role": "user", "content": request.user}],
        }).encode("utf-8"),
        accept="application/json",
        contentType="application/json",
    )
    raw = json.loads(response["body"].read())
    return normalize_text(raw.get("content", raw))
