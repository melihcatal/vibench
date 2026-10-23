from vision_client import build_openai_client, load_vision_config, chat_text_completion


def visual_safety_text(text: str):
    config = load_vision_config("gpt-4o-mini")
    client = build_openai_client(config.api_key)
    prompt = f"Check this visual analysis text for unsafe or policy-sensitive wording. Return SAFE or UNSAFE with a brief reason:\n{text}"
    return chat_text_completion(client, config.model, prompt, max_tokens=120)
