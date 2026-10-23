from vision_client import build_openai_client, load_vision_config, chat_vision_completion
from vision_models import normalize_text


def detect_image_text(image_path: str):
    config = load_vision_config("gpt-4o-mini")
    client = build_openai_client(config.api_key)
    text = chat_vision_completion(client, config.model, "Extract all visible text from this image, preserving line breaks as best you can.", image_path, max_tokens=200)
    return normalize_text(text)
