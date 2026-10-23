from openai import OpenAI

from model_client import get_client, select_text_model
from model_models import CompletionRequest


PROVIDER = "openai"
DEFAULT_MODEL = "gpt-4o-mini"


def stream_completion(prompt: str):
    client = get_client()
    model = select_text_model(default=DEFAULT_MODEL)
    req = CompletionRequest(
        model=model,
        messages=[
            {"role": "system", "content": "Stream a direct, helpful completion."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.3,
        stream=True,
    )
    return client.chat.completions.create(**req.to_openai_kwargs())
