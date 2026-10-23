from typing import Generator
from model_client import GeminiClient
from model_models import ModelPayload, ModelResponse

def stream_completion(payload: ModelPayload) -> Generator[ModelResponse, None, None]:
    client = GeminiClient()
    model = client.get_generative_model(model_name="gemini-pro")
    
    prompt = f"Continue the following text: {payload.text}"
    
    responses = model.generate_content(prompt, stream=True)
    
    for chunk in responses:
        yield ModelResponse(text=chunk.text)
