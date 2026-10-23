from model_client import stream_chat
from model_models import LLMRequest

STREAM_MODEL = "gpt-4o-mini"


def stream_completion(prompt: str):
    request = LLMRequest(
        prompt=prompt,
        system="You are a responsive assistant that streams concise completions.",
        model=STREAM_MODEL,
        temperature=0.2,
        max_tokens=256,
    )
    for token in stream_chat(request):
        yield token
