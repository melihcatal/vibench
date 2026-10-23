from model_client import ANTHROPIC_API_URL, ANTHROPIC_API_KEY
from model_models import ModelRequest, ModelResponse


def answer_with_context(question, context):
    headers = {
        "Authorization": f"Bearer {ANTHROPIC_API_KEY}",
        "Content-Type": "application/json",
    }
    data = {
        "prompt": f"Answer the following question using the provided context: {question}. Context: {context}",
        "max_tokens_to_sample": 100,
    }
    response = requests.post(ANTHROPIC_API_URL, headers=headers, json=data)
    return ModelResponse(response.json()["completion"])
