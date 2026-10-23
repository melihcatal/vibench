from typing import Optional

from model_client import get_client, resolve_model_name
from model_models import normalize_text


def localized_platform_output(text: str, target_locale: str, model: Optional[str] = None) -> str:
    client = get_client()
    model_name = resolve_model_name(model)
    response = client.responses.create(
        model=model_name,
        input=[
            {"role": "system", "content": f"Translate the following content into {target_locale}. Preserve meaning and tone."},
            {"role": "user", "content": normalize_text(text)},
        ],
        temperature=0.1,
        max_output_tokens=512,
    )
    return getattr(response, "output_text", "") or ""
