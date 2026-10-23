from google import genai

from model_client import get_api_key, get_model


def answer_with_context(payload, config=None):
    config = config or {}
    prompt = "Context:\n" + payload["context"] + "\n\nQuestion:\n" + payload["question"]
    with genai.Client(api_key=get_api_key(config)) as client:
        response = client.models.generate_content(model=get_model(config), contents=prompt)
    return {"answer": response.text or ""}
