import os
import vertexai
from vertexai.preview.generative_models import GenerativeModel, Part
from typing import Iterator

PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT")
LOCATION = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")

def stream_platform_generation(prompt: str) -> Iterator[Part]:
    vertexai.init(project=PROJECT_ID, location=LOCATION)
    model = GenerativeModel("gemini-pro")
    responses = model.generate_content(prompt, stream=True)
    for response in responses:
        yield response.candidates[0].content.parts[0]