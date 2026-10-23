from typing import Iterator
from vertexai.preview.language_models import TextGenerationModel

from model_client import get_palm_model

def stream_completion(prompt: str) -> Iterator[str]:
    model = get_palm_model()
    responses = model.predict_streaming(
        prompt,
        temperature=0.7,
        max_output_tokens=512,
    )
    for response in responses:
        yield response.text
