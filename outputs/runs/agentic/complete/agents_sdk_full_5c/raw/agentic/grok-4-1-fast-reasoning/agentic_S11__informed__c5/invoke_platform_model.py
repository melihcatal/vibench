from model_client import get_client
from model_models import build_chat_messages

def invoke_platform_model(prompt: str, deployment_id: str = 'gpt-4o-mini') -> str:
    client = get_client()
    messages = build_chat_messages(prompt)
    response = client.chat.completions.create(
        model=deployment_id,
        messages=messages,
    )
    return response.choices[0].message.content
