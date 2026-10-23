from model_client import get_client
from model_models import build_chat_messages

def stream_platform_generation(prompt: str, deployment_id: str = 'gpt-4o-mini'):
    client = get_client()
    messages = build_chat_messages(prompt)
    response = client.chat.completions.create(
        model=deployment_id,
        messages=messages,
        stream=True,
    )
    for chunk in response:
        yield chunk
