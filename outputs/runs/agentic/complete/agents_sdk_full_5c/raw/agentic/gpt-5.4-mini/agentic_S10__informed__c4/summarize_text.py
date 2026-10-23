from __future__ import annotations

from model_client import get_client, load_config, choose_model
from model_models import PromptRequest, response_to_normalized

SYSTEM_PROMPT = "You are a concise summarizer. Summarize the user's text faithfully and clearly."


def summarize_text(long_text: str) -> str:
    config = load_config()
    client = get_client(config)
    model = choose_model("summarize", config)
    request = PromptRequest(text=long_text, system=SYSTEM_PROMPT)
    response = client.chat.completions.create(
        model=model,
        temperature=config.temperature,
        messages=[
            {"role": "system", "content": request.system},
            {"role": "user", "content": request.text},
        ],
    )
    return response_to_normalized(response, model).text
