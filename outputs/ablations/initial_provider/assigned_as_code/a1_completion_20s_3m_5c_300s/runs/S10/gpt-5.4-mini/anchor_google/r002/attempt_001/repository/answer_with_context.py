from model_client import generate_text
from model_models import normalize_text_response


def answer_with_context(payload, config=None):
    prompt = "Answer the question using only the provided context.\n\nContext:\n" + payload["context"] + "\n\nQuestion:\n" + payload["question"]
    response = generate_text(prompt, config=config)
    return normalize_text_response(response)
