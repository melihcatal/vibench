from __future__ import annotations

from typing import Optional

from openai import OpenAI

from model_client import build_client, model_for_task
from model_models import ChatRequest, normalize_text


OPENAI_TTS_TEXT_MODEL = "gpt-4o-mini"
OPENAI_TTS_AUDIO_MODEL = "gpt-4o-mini-tts"


def spoken_brief(text: str, client: Optional[OpenAI] = None) -> str:
    client = client or build_client()
    request = ChatRequest(
        task="spoken_brief",
        model=model_for_task("spoken_brief", default=OPENAI_TTS_TEXT_MODEL),
        system_prompt="Create a short spoken brief from the provided text.",
        user_prompt=f"Turn the following into a concise spoken brief:\n\n{text}",
    )
    response = client.chat.completions.create(model=request.model, messages=request.messages(), temperature=0.4)
    return normalize_text(response.choices[0].message.content or "")
