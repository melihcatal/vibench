import vertexai
from vertexai.preview.language_models import TextGenerationModel
from typing import Iterator

def stream_platform_generation(project_id: str, location: str, model_id: str, prompt: str) -> Iterator[str]:
    """Streams output from a Google Cloud Vertex AI model, preserving provider response objects."""
    vertexai.init(project=project_id, location=location)
    model = TextGenerationModel.from_pretrained(model_id)
    
    # The stream method returns an Iterable of TextGenerationResponse objects
    # We'll yield the text content from each part.
    for response_part in model.stream_predict(prompt=prompt):
        yield response_part.text
