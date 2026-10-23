from model_client import get_client
from model_models import build_messages, stream_tokens

def stream_completion(system_prompt: str, user_prompt: str):
    client = get_client()
    messages = build_messages(system_prompt, user_prompt)
    yield from stream_tokens(client, messages)