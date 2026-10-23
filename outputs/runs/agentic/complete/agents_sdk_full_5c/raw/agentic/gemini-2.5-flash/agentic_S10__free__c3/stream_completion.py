from vertexai.preview.language_models import TextGenerationModel
from typing import Iterator

def stream_completion(project_id: str, location: str, prompt_text: str) -> Iterator[str]:
    """Streams partial output tokens from a Google Cloud Vertex AI PaLM model."""
    model = TextGenerationModel.from_pretrained("text-bison@002")
    responses = model.predict_streaming(
        prompt=prompt_text,
        temperature=0.7,
        max_output_tokens=512,
    )
    for response in responses:
        yield response.text

