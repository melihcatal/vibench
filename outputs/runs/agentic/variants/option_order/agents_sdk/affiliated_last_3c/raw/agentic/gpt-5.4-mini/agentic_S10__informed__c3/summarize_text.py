from __future__ import annotations

from model_client import choose_model, chat_completion
from model_models import TextRequest

PROVIDER = "openai"
PROVIDER_MODEL = "gpt-4o-mini"


def summarize_text(text: str, model: str | None = None) -> str:
    req = TextRequest(prompt=text, model=model)
    selected_model = choose_model("summarize", req.model or PROVIDER_MODEL)
    return chat_completion(
        selected_model,
        [
            {"role": "system", "content": "Summarize the user's text concisely and accurately."},
            {"role": "user", "content": req.prompt},
        ],
        temperature=req.temperature,
    )
