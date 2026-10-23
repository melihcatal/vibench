from __future__ import annotations

from openai import OpenAI

from model_client import LLMConfig, get_openai_client
from model_models import ContextQuestionRequest, TextResponse

ANSWER_MODEL = "gpt-4.1-mini"


def answer_with_context(context: str, question: str, client: OpenAI | None = None) -> TextResponse:
    cfg = LLMConfig(chat_model=ANSWER_MODEL)
    llm = client or get_openai_client(cfg)
    req = ContextQuestionRequest(context=context, question=question, max_output_tokens=240, temperature=0.1)
    completion = llm.chat.completions.create(
        model=cfg.chat_model,
        messages=[
            {"role": "system", "content": "Answer using only the provided context when possible."},
            {"role": "user", "content": f"Context:\n{req.context}\n\nQuestion:\n{req.question}"},
        ],
        temperature=req.temperature,
        max_tokens=req.max_output_tokens,
    )
    return TextResponse(text=completion.choices[0].message.content or "", model=cfg.chat_model, raw=completion.model_dump())
