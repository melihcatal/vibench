from model_client import client

def is_safe(content: str) -> bool:
    """
    Check prompts and generated text for unsafe content using OpenAI Moderation API.
    """
    response = client.moderations.create(input=content)
    return not response.results[0].flagged