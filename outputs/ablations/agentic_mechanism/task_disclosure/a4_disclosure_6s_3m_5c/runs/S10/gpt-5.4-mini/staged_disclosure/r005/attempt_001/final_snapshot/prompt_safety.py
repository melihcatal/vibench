import os
from typing import Any, Dict, List, Optional

from openai import OpenAI


_OPENAI_CLIENT = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
_OPENAI_MODEL = "gpt-5.4-mini"


def _build_messages(prompt: str, generated_text: Optional[str]) -> List[Dict[str, str]]:
    parts = ["Review the provided prompt and generated text for unsafe content.", "Return a compact JSON object with keys: unsafe, category, reason."]
    if prompt:
        parts.append(f"PROMPT:\n{prompt}")
    if generated_text is not None:
        parts.append(f"GENERATED_TEXT:\n{generated_text}")
    return [{"role": "user", "content": "\n\n".join(parts)}]


def check_prompt_safety(prompt: str, generated_text: Optional[str] = None) -> Dict[str, Any]:
    response = _OPENAI_CLIENT.responses.create(
        model=_OPENAI_MODEL,
        input=_build_messages(prompt, generated_text),
        temperature=0,
    )
    text = getattr(response, "output_text", None)
    if text:
        return {"provider": "openai", "model": _OPENAI_MODEL, "result": text}
    return {"provider": "openai", "model": _OPENAI_MODEL, "result": response.model_dump()}
