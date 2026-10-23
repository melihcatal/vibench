import os
from typing import Iterator
from model_client import VertexAIModelClient
from model_models import InferenceRequest, InferenceResponse
from vertexai.preview.generative_models import GenerationResponse


def stream_completion(request: InferenceRequest) -> Iterator[InferenceResponse]:
    """Streams partial output tokens from a hosted LLM."""
    client = VertexAIModelClient(
        model_name="gemini-pro"
    )  # Using google.cloud.aiplatform via VertexAIModelClient

    responses_iterator = client.stream_generate_text(
        request.prompt,
        max_output_tokens=request.max_output_tokens,
        temperature=request.temperature,
        top_p=request.top_p,
        top_k=request.top_k,
    )

    for response in responses_iterator:
        generated_text = ""
        safety_attributes = None

        if response.candidates:
            generated_text = response.candidates[0].content.parts[0].text
            safety_attributes = {
                "safety_ratings": [
                    sr.to_dict() for sr in response.candidates[0].safety_ratings
                ]
            }

        yield InferenceResponse(
            generated_text=generated_text, safety_attributes=safety_attributes
        )
