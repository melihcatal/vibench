from vision_client import build_openai_client, load_vision_config, chat_vision_completion
from vision_models import normalize_text


def describe_image(image_path: str):
    config = load_vision_config("gpt-4o-mini")
    client = build_openai_client(config.api_key)
    text = chat_vision_completion(client, config.model, "Write a short, vivid description of this image in one sentence.", image_path, max_tokens=120)
    return normalize_text(text)
