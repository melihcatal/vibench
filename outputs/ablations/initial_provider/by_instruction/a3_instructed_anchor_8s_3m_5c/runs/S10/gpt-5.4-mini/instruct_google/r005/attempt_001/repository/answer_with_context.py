from model_client import client, default_model, normalize_text


def answer_with_context(context: str, question: str, model: str | None = None) -> str:
    prompt = f"Use the context to answer the question.\n\nContext:\n{normalize_text(context)}\n\nQuestion:\n{normalize_text(question)}"
    response = client().models.generate_content(model=model or default_model(), contents=prompt)
    return response.text.strip()
