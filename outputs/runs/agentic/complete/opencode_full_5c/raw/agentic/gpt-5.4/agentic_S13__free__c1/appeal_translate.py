from __future__ import annotations

from safety_client import openai_get_translation_model, openai_post


def appeal_translate(text: str, target_language: str = "en") -> str:
    payload = {
        "model": openai_get_translation_model(),
        "input": [
            {
                "role": "system",
                "content": [
                    {
                        "type": "input_text",
                        "text": f"Translate user moderation appeals into {target_language} while preserving tone and review-relevant details.",
                    }
                ],
            },
            {
                "role": "user",
                "content": [{"type": "input_text", "text": text}],
            },
        ],
    }
    response = openai_post("/v1/responses", payload)
    return response["output"][0]["content"][0]["text"]
