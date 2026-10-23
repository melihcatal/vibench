from model_client import client_from_config, get_model_name


def answer_with_context(payload, config=None):
    config = config or {}
    context = payload.get("context", "")
    question = payload["question"]
    prompt = "Use the context to answer the question.\n\nContext:\n" + context + "\n\nQuestion:\n" + question
    with client_from_config(config) as client:
        response = client.models.generate_content(model=get_model_name(config), contents=prompt)
    return {"text": response.text or ""}
