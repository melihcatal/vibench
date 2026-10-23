from openai import OpenAI

from model_client import get_client, select_reasoning_model
from model_models import CompletionRequest, CompletionResponse, normalize_completion_response


PROVIDER = "openai"
DEFAULT_MODEL = "gpt-4o-mini"


def answer_with_context(question: str, context: str) -> CompletionResponse:
    client = get_client()
    model = select_reasoning_model(default=DEFAULT_MODEL)
    req = CompletionRequest(
        model=model,
        messages=[
            {"role": "system", "content": "Answer using only the supplied context. If missing, say you do not know."},
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion:\n{question}"},
        ],
        temperature=0.1,
    )
    resp = client.chat.completions.create(**req.to_openai_kwargs())
    return normalize_completion_response(resp)
