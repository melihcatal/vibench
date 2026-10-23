import os
from typing import Any, Dict
from model_client import GeminiClient

def result_translate(payload: Dict[str, Any], config: Dict[str, Any] = None) -> Dict[str, Any]:
    config = config or {}
    client = GeminiClient(api_key=config.get("api_key"))
    model = client.get_model("gemini-1.5-pro") # Good for translation and complex tasks

    text_to_translate = payload.get("text", "")
    target_language = payload.get("target_language", "English") # Default to English

    if not text_to_translate:
        raise ValueError("Payload must contain 'text' for translation.")

    prompt = (
        f"Translate the following text into {target_language}. "
        f"Only provide the translated text.\n\nText: {text_to_translate}"
    )

    response = model.generate_content(prompt)
    return {"translated_text": response.text.strip()}
