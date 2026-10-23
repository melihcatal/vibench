from __future__ import annotations

from openai import OpenAI

from model_client import LLMConfig, get_openai_client
from model_models import TextRequest, TextResponse

SUMMARY_MODEL = "gpt-4.1-mini"


def summarize_text(text: str, client: OpenAI | None = None) -> TextResponse:
    cfg = LLMConfig(chat_model=SUMMARY_MODEL)
    llm = client or get_openai_client(cfg)
    req = TextRequest(text=text, max_output_tokens=220, temperature=0.2)
    completion = llm.chat.completions.create(
        model=cfg.chat_model,
        messages=[
            {"role": "system", "content": "You are a concise summarization assistant."},
            {"role": "user", "content": f"Summarize the following text:\n\n{req.text}"},
        ],
        temperature=req.temperature,
        max_tokens=req.max_output_tokens,
    )
    return TextResponse(text=completion.choices[0].message.content or "", model=cfg.chat_model, raw=completion.model_dump())
