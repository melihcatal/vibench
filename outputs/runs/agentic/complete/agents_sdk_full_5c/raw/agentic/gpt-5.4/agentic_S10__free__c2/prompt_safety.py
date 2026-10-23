from __future__ import annotations

from model_client import moderate_text


def check_prompt_and_output(prompt: str, generated_text: str) -> dict:
    prompt_result = moderate_text(prompt)
    output_result = moderate_text(generated_text)
    return {
        "provider": "openai",
        "moderation_model": "omni-moderation-latest",
        "prompt": {
            "flagged": prompt_result.flagged,
            "categories": prompt_result.categories,
        },
        "generated_text": {
            "flagged": output_result.flagged,
            "categories": output_result.categories,
        },
        "unsafe": prompt_result.flagged or output_result.flagged,
    }
