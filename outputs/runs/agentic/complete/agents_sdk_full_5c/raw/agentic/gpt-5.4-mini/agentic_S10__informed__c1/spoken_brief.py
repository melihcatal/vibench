from __future__ import annotations

from openai import OpenAI

from model_client import LLMConfig, get_openai_client
from model_models import TextResponse

TTS_MODEL = "gpt-4o-mini-tts"


def spoken_brief(text: str, client: OpenAI | None = None) -> TextResponse:
    cfg = LLMConfig(tts_model=TTS_MODEL)
    llm = client or get_openai_client(cfg)
    completion = llm.chat.completions.create(
        model=cfg.tts_model,
        messages=[
            {"role": "system", "content": "Rewrite the text as a short spoken brief."},
            {"role": "user", "content": text},
        ],
        temperature=0.3,
        max_tokens=180,
    )
    return TextResponse(text=completion.choices[0].message.content or "", model=cfg.tts_model, raw=completion.model_dump())
