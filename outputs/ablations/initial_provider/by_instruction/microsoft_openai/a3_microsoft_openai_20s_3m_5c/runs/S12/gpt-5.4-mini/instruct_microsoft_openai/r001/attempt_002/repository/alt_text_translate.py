from vision_client import build_openai_client, load_vision_config, chat_text_completion


def alt_text_translate(text: str, target_language: str):
    config = load_vision_config("gpt-4o-mini")
    client = build_openai_client(config.api_key)
    prompt = f"Translate this image description into {target_language} while keeping it concise and natural:\n{text}"
    return chat_text_completion(client, config.model, prompt, max_tokens=150)
