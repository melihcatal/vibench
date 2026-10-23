from.safety_client import get_client

def create_moderation_request(text):
    client = get_client()
    return client.completions.create(
        model='text-moderation-001',
        prompt=text,
        max_tokens=100
    )