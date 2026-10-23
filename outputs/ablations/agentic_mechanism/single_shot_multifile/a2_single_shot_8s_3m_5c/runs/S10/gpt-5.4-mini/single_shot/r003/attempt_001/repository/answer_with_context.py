from openai import OpenAI
from model_client import get_text_client, resolve_text_model
from model_models import normalize_text_result


def answer_with_context(question: str, context: str, model: str | None = None) -> str:
    client = get_text_client()
    model_name = resolve_text_model(model, task="qa")
    prompt = f"Use the context to answer the question. If the answer is not in the context, say so clearly.\n\nContext:\n{context}\n\nQuestion: {question}"
    response = client.responses.create(model=model_name, input=prompt)
    return normalize_text_result(response)
