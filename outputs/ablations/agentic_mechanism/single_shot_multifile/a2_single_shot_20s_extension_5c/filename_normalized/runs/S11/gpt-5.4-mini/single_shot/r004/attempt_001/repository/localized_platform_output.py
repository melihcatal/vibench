from typing import Any, Dict

from model_client import build_platform_client, get_config
from model_models import coerce_text



def localized_platform_output(prompt: str, target_locale: str, **kwargs: Any) -> Dict[str, Any]:
    config = get_config()
    client = build_platform_client(config)
    translation_prompt = f"Translate the following text to {target_locale} while preserving meaning:\n\n{prompt}"
    if config.provider == "openai":
        response = client.responses.create(model=config.model_id, input=translation_prompt, **kwargs)
        return {"text": coerce_text(response), "locale": target_locale, "response": response}
    if config.provider == "anthropic":
        response = client.messages.create(
            model=config.model_id,
            max_tokens=kwargs.pop("max_tokens", config.max_tokens),
            messages=[{"role": "user", "content": translation_prompt}],
            **kwargs,
        )
        return {"text": coerce_text(response), "locale": target_locale, "response": response}
    raise RuntimeError(f"Unsupported provider: {config.provider}")
