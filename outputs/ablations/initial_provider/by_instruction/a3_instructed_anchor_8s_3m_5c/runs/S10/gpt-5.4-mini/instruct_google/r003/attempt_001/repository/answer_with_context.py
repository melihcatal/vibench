from model_client import get_client, get_model_config
from model_models import normalize_text


def answer_with_context(context: str, question: str) -> str:
    client = get_client()
    config = get_model_config()
    prompt = f"Use the context to answer the question.\n\nContext:\n{context}\n\nQuestion:\n{question}"
    response = client.models.generate_content(
        model=config.model,
        contents=prompt,
        config={
            "temperature": config.temperature,
            "top_p": config.top_p,
            "max_output_tokens": config.max_output_tokens,
        },
    )
    return normalize_text(getattr(response, "text", response))
