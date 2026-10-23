from model_client import get_client
from model_models import build_chat_messages

def collect_platform_metadata(prompt: str, deployment_id: str = 'gpt-4o-mini') -> dict:
    client = get_client()
    messages = build_chat_messages(prompt)
    response = client.chat.completions.create(
        model=deployment_id,
        messages=messages,
    )
    return {
        'output': response.choices[0].message.content,
        'metadata': {
            'model': response.model,
            'usage': {
                'prompt_tokens': response.usage.prompt_tokens if response.usage else 0,
                'completion_tokens': response.usage.completion_tokens if response.usage else 0,
                'total_tokens': response.usage.total_tokens if response.usage else 0,
            },
            'id': response.id,
            'finish_reason': response.choices[0].finish_reason,
        }
    }
