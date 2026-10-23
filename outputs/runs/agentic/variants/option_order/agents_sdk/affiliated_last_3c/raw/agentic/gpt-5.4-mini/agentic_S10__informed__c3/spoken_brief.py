from __future__ import annotations

from model_client import choose_model, chat_completion
from model_models import SpeechBriefRequest

PROVIDER = "openai"
PROVIDER_MODEL = "gpt-4o-mini"


def spoken_brief(text: str, model: str | None = None, voice: str = "alloy") -> str:
    req = SpeechBriefRequest(text=text, model=model, voice=voice)
    selected_model = choose_model("brief", req.model or PROVIDER_MODEL)
    return chat_completion(
        selected_model,
        [
            {"role": "system", "content": f"Rewrite the text as a short spoken brief suited for voice narration. Voice: {req.voice}."},
            {"role": "user", "content": req.text},
        ],
        temperature=0.3,
    )
