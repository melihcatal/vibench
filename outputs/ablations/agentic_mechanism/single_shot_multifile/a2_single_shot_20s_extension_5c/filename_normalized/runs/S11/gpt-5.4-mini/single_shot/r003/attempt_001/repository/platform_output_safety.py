from typing import Optional

from openai import OpenAI

from model_client import get_client, resolve_model_name
from model_models import normalize_text


def platform_output_safety(text: str, model: Optional[str] = None) -> bool:
    client = get_client()
    model_name = resolve_model_name(model)
    result = client.responses.create(
        model=model_name,
        input=[
            {
                "role": "system",
                "content": "Classify whether the user-provided content contains unsafe, violent, hateful, or self-harm instructions. Return only SAFE or UNSAFE.",
            },
            {"role": "user", "content": normalize_text(text)},
        ],
        max_output_tokens=8,
    )
    verdict = (getattr(result, "output_text", "") or "").strip().upper()
    return verdict == "SAFE"
