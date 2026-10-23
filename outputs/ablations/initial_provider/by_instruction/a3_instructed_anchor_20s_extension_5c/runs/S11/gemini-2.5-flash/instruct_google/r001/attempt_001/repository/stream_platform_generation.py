from google.cloud import aiplatform
from vertexai.preview.language_models import TextGenerationModel
from typing import Iterator

def stream_platform_generation(project_id: str, location: str, model_id: str, prompt: str) -> Iterator[str]:
    """
    Streams output from a Google Cloud Vertex AI generative model.
    """
    aiplatform.init(project=project_id, location=location)
    
    text_model = TextGenerationModel.from_pretrained(model_id)
    
    responses = text_model.predict_streaming(prompt=prompt)
    
    for response in responses:
        yield response.text
