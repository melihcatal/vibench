def select_platform_resource(model_type: str = "chat") -> str:
    if model_type == "chat":
        return "gpt-4o"  # OpenAI's flagship model
    elif model_type == "embedding":
        return "text-embedding-3-small"
    elif model_type == "moderation":
        return "text-moderation-latest"
    elif model_type == "tts":
        return "tts-1"
    return "gpt-3.5-turbo"
