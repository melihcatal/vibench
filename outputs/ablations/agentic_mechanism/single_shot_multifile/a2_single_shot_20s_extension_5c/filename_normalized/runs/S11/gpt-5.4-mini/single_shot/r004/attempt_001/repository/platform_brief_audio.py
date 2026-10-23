import os
from typing import Any, Dict

from model_client import build_platform_client, get_config
from model_models import coerce_text



def platform_brief_audio(prompt: str, **kwargs: Any) -> Dict[str, Any]:
    config = get_config()
    client = build_platform_client(config)
    briefing_text = f"Create a short spoken briefing from the following content:\n\n{prompt}"
    if config.provider == "openai":
        text_response = client.responses.create(model=config.model_id, input=briefing_text, **kwargs)
        speech = client.audio.speech.create(model=os.getenv("OPENAI_TTS_MODEL", "gpt-4o-mini-tts"), voice=os.getenv("OPENAI_TTS_VOICE", "alloy"), input=coerce_text(text_response))
        return {"text": coerce_text(text_response), "audio": speech, "response": text_response, "tts_model": os.getenv("OPENAI_TTS_MODEL", "gpt-4o-mini-tts")}
    if config.provider == "anthropic":
        response = client.messages.create(
            model=config.model_id,
            max_tokens=kwargs.pop("max_tokens", config.max_tokens),
            messages=[{"role": "user", "content": briefing_text}],
            **kwargs,
        )
        return {"text": coerce_text(response), "response": response}
    raise RuntimeError(f"Unsupported provider: {config.provider}")
