from vision_client import build_openai_client, load_vision_config, chat_vision_completion


def score_image_safety(image_path: str):
    config = load_vision_config("gpt-4o-mini")
    client = build_openai_client(config.api_key)
    text = chat_vision_completion(client, config.model, "Assess whether this image contains unsafe or policy-sensitive content. Answer with SAFE or UNSAFE and a brief reason.", image_path, max_tokens=120)
    return text
