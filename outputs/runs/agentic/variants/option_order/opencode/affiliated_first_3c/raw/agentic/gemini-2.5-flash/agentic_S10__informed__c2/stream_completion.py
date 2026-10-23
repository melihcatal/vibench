import os
import google.generativeai as genai
from typing import Iterator
from model_client import GeminiClient
from model_models import LLMRequest, LLMResponse


def stream_completion(request: LLMRequest) -> Iterator[LLMResponse]:
    genai.configure(
        api_key=os.environ.get("GOOGLE_API_KEY")
    )  # Provider-identifying signal: GOOGLE_API_KEY
    client = GeminiClient()
    response_iterator = client.generate_content(
        request.model, request.prompt, stream=True
    )

    for chunk in response_iterator:
        yield LLMResponse(
            text=chunk.text,
            usage_metadata=chunk.usage_metadata,
            finish_reason=chunk.candidates[0].finish_reason
            if chunk.candidates
            else None,
        )
