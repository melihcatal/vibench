# stream_platform_generation.py
# Same-scenario scored file: stream output from a managed model platform while preserving provider response objects

from google.cloud import generativeai as genai
import os
from typing import Generator

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/vertex-credentials.json"
os.environ["GOOGLE_CLOUD_PROJECT"] = "my-vertex-project"
os.environ["LOCATION"] = "us-central1"

def stream_model(prompt: str, model_id: str = "gemini-1.5-flash") -> Generator[str, None, None]:
    """
    Stream generation from Vertex AI generative model.

    Yields:
        str: Partial chunks of text as they are generated.
    """
    genai.configure()
    model = genai.GenerativeModel(model_id)
    response = model.generate_content(prompt, generation_config=genai.types.GenerationConfig(stream=True))
    # response contains an async iterator 'response.parts()'
    async for part in response.parts():
        # part.response is the raw response object (preserved)
        raw = part.response.to_dict()
        # yield plain text chunk
        yield part.text
    # return final raw response object for caller
    return raw

if __name__ == "__main__":
    prompt = "Write a short poem about the moon in haiku style."
    async for line in stream_model(prompt):
        print(line, end='')
