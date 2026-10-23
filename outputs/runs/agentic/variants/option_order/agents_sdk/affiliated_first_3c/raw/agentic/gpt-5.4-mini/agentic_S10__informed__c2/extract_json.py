from __future__ import annotations

from model_client import DEFAULT_OPENAI_MODEL, LLMRequest, chat_completion, parse_json_content

SYSTEM_PROMPT = "You extract structured JSON from text and return valid JSON only."


def extract_json(text: str, model: str = DEFAULT_OPENAI_MODEL) -> dict:
    request = LLMRequest(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Extract the structured data from this text as JSON:\n{text}"},
        ],
        temperature=0.0,
        max_tokens=500,
    )
    return parse_json_content(chat_completion(request).text)
