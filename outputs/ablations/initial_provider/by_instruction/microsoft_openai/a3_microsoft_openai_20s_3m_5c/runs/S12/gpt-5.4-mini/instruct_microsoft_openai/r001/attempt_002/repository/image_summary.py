from vision_client import build_openai_client, load_vision_config, chat_text_completion


def image_summary(analysis_text: str):
    config = load_vision_config("gpt-4o-mini")
    client = build_openai_client(config.api_key)
    return chat_text_completion(client, config.model, f"Summarize the following visual analysis in one concise paragraph:\n{analysis_text}", max_tokens=150)
