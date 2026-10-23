from vision_client import build_openai_client, load_vision_config, chat_vision_completion
from vision_models import normalize_labels


def detect_image_labels(image_path: str):
    config = load_vision_config("gpt-4o-mini")
    client = build_openai_client(config.api_key)
    text = chat_vision_completion(
        client,
        config.model,
        "List the main objects, entities, and visual labels in this image as comma-separated terms.",
        image_path,
        max_tokens=200,
    )
    return normalize_labels(text)
