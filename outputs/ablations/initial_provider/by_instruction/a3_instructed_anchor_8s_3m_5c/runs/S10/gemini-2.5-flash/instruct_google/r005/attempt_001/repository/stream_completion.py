from model_client import get_generative_model
from typing import Iterator

def stream_completion(prompt: str) -> Iterator[str]:
    model = get_generative_model("gemini-pro")
    response = model.generate_content(prompt, stream=True)
    for chunk in response:
        yield chunk.text
