import os
from google.cloud import aiplatform
from google.generativeai import GenerativeModel, configure
from typing import Iterator

def stream_completion(prompt: str) -> Iterator[str]:
    """
    Streams partial output tokens from a Google Generative AI model.
    """
    # Configure the Google Generative AI client
    # configure(api_key=os.environ.get("GOOGLE_API_KEY"))

    # For Vertex AI:
    # aiplatform.init(project=os.environ.get("GOOGLE_CLOUD_PROJECT"), location=os.environ.get("GOOGLE_CLOUD_LOCATION"))
    # model = GenerativeModel(model_name="gemini-pro")

    # For Gemini API
    model = GenerativeModel(model_name="gemini-pro")

    responses = model.generate_content(prompt, stream=True)
    for response in responses:
        yield response.text
