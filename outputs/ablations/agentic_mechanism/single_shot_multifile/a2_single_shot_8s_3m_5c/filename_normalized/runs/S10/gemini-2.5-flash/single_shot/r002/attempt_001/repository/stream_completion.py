import os
import vertexai
from vertexai.generative_models import GenerativeModel
from model_client import get_gemini_model
from typing import Iterator

def stream_completion(prompt: str) -> Iterator[str]:
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
    location = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")
    
    model = get_gemini_model(project_id, location, "gemini-pro")
    
    responses = model.generate_content(
        contents=prompt,
        stream=True,
        generation_config={
            "temperature": 0.8,
            "top_p": 0.95,
        }
    )
    
    for response in responses:
        if response.text:
            yield response.text
