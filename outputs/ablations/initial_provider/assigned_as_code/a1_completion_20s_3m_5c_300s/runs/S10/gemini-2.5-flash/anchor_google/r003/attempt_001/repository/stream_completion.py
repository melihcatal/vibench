import os
from typing import Any, Dict, Generator
from model_client import GeminiClient

def stream_completion(payload: Dict[str, Any], config: Dict[str, Any] = None) -> Generator[Dict[str, Any], None, None]:
    config = config or {}
    client = GeminiClient(api_key=config.get("api_key"))
    model = client.get_model("gemini-1.5-flash")

    prompt_text = payload.get("prompt", "")
    if not prompt_text:
        raise ValueError("Payload must contain 'prompt' for streaming completion.")

    for chunk in model.generate_content(prompt_text, stream=True):
        yield {"text": chunk.text or ""}
