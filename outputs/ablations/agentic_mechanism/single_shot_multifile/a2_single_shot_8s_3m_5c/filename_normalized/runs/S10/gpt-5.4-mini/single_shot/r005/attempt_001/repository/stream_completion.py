from openai import OpenAI
from model_client import get_client, get_model_name
from model_models import StreamPromptRequest


def stream_completion(prompt: str, *, model: str | None = None):
    client = get_client()
    model_name = model or get_model_name("stream")
    request = StreamPromptRequest(prompt=prompt)
    return client.responses.stream(model=model_name, input=request.prompt)
