from model_client import GeminiClient
from model_models import LLMRequest
from typing import Iterator

def stream_completion(request: LLMRequest) -> Iterator[str]:
    client = GeminiClient()
    model = client.get_generative_model(request.model_id)

    generation_config = {
        "max_output_tokens": request.max_output_tokens or 500,
        "temperature": request.temperature or 0.7,
        "top_p": request.top_p or 1,
        "top_k": request.top_k or 1
    }

    prompt = f"Continue the following text:\n\n{request.text}"

    response_stream = model.generate_content(prompt, generation_config=generation_config, stream=True)

    for chunk in response_stream:
        yield chunk.text
