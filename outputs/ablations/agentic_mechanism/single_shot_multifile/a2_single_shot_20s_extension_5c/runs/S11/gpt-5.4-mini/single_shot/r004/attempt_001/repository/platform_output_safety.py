from typing import Any, Dict

from model_client import build_platform_client, get_config
from model_models import coerce_text



def platform_output_safety(prompt: str, **kwargs: Any) -> Dict[str, Any]:
    config = get_config()
    client = build_platform_client(config)
    if config.provider == "openai":
        response = client.responses.create(model=config.model_id, input=prompt, **kwargs)
        text = coerce_text(response)
        moderation = client.moderations.create(input=text)
        flagged = bool(getattr(moderation.results[0], "flagged", False)) if getattr(moderation, "results", None) else False
        return {"text": text, "flagged": flagged, "moderation": moderation, "response": response}
    if config.provider == "anthropic":
        response = client.messages.create(
            model=config.model_id,
            max_tokens=kwargs.pop("max_tokens", config.max_tokens),
            messages=[{"role": "user", "content": prompt}],
            **kwargs,
        )
        text = coerce_text(response)
        flagged = any(term in text.lower() for term in ("self-harm", "violence", "weapon"))
        return {"text": text, "flagged": flagged, "response": response}
    raise RuntimeError(f"Unsupported provider: {config.provider}")
