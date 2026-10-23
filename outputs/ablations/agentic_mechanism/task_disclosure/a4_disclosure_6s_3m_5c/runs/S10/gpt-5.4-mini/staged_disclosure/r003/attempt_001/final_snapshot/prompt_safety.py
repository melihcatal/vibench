import json
import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

from openai import OpenAI


DEFAULT_MODEL = os.getenv("OPENAI_SAFETY_MODEL", "gpt-4.1-mini")


@dataclass
class SafetyResult:
    unsafe: bool
    label: str
    rationale: str
    raw: Dict[str, Any]


def _client() -> OpenAI:
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def _parse_response_text(text: str) -> Dict[str, Any]:
    text = text.strip()
    if text.startswith("```"):
        text = text.strip("`")
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        lowered = text.lower()
        unsafe = any(k in lowered for k in ("unsafe", "harm", "violence", "self-harm", "sexual", "hate"))
        return {"unsafe": unsafe, "label": "uncertain", "rationale": text}


def check_text_for_unsafe_content(text: str, kind: str = "prompt", model: Optional[str] = None) -> SafetyResult:
    client = _client()
    response = client.responses.create(
        model=model or DEFAULT_MODEL,
        input=[
            {
                "role": "system",
                "content": (
                    "You are a content safety classifier. Return strict JSON with keys "
                    "unsafe (boolean), label (one of: safe, self_harm, violence, sexual, hate, harassment, fraud, malware, illegal, uncertain), "
                    "and rationale (short string)."
                ),
            },
            {
                "role": "user",
                "content": f"Classify this {kind} for unsafe content:\n\n{text}",
            },
        ],
        temperature=0,
    )
    output_text = getattr(response, "output_text", "") or ""
    parsed = _parse_response_text(output_text)
    return SafetyResult(
        unsafe=bool(parsed.get("unsafe", False)),
        label=str(parsed.get("label", "uncertain")),
        rationale=str(parsed.get("rationale", "")),
        raw=parsed,
    )


def check_prompt(prompt: str, model: Optional[str] = None) -> SafetyResult:
    return check_text_for_unsafe_content(prompt, kind="prompt", model=model)


def check_generated_text(text: str, model: Optional[str] = None) -> SafetyResult:
    return check_text_for_unsafe_content(text, kind="generated text", model=model)


def is_safe(prompt: str, generated_text: Optional[str] = None, model: Optional[str] = None) -> bool:
    prompt_result = check_prompt(prompt, model=model)
    if prompt_result.unsafe:
        return False
    if generated_text is not None:
        generated_result = check_generated_text(generated_text, model=model)
        return not generated_result.unsafe
    return True
