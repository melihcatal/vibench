import typing
from model_client import LLMClient

def stream_completion(prompt: str) -> typing.Iterator[str]:
    client = LLMClient()
    model = client.get_model()
    responses = model.generate_content(prompt, stream=True)
    for chunk in responses:
        yield chunk.text
