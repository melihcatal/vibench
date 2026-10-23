import os


def get_api_key() -> str:
    return os.getenv("DASHSCOPE_API_KEY")


def create_client() -> TextEmbedding:
    api_key = get_api_key()
    if not api_key:
        raise ValueError("DASHSCOPE_API_KEY environment variable not set")
    return TextEmbedding(api_key=api_key)
