from model_client import ManagedModelClient


def check_platform_output_safety(output: str) -> bool:
    # Concrete provider: OpenAI Moderation (supported by openai library)
    client = ManagedModelClient(provider="openai")
    safe = client.is_safe(output)
    return safe
