import os
import json
from model_client import VertexAIModelClient
from model_models import InferenceRequest, InferenceResponse


def extract_json(request: InferenceRequest) -> InferenceResponse:
    """Calls a hosted LLM to extract structured JSON from text."""
    client = VertexAIModelClient(
        model_name="gemini-pro"
    )  # Using google.cloud.aiplatform via VertexAIModelClient

    prompt = (
        f"Extract information from the following text into a JSON object. "
        f"The JSON should contain relevant fields based on the text content. "
        f"Ensure the output is valid JSON only.\n\nText: {request.prompt}\n\nJSON:"
    )

    response = client.generate_text(
        prompt,
        max_output_tokens=request.max_output_tokens,
        temperature=request.temperature,
        top_p=request.top_p,
        top_k=request.top_k,
    )

    generated_text = ""
    safety_attributes = None

    if response.candidates:
        generated_text = response.candidates[0].content.parts[0].text
        safety_attributes = {
            "safety_ratings": [
                sr.to_dict() for sr in response.candidates[0].safety_ratings
            ]
        }

        # Attempt to parse and validate JSON
        try:
            json.loads(generated_text)
        except json.JSONDecodeError:
            # If it's not valid JSON, we might want to log an error or retry
            # For this exercise, we'll return the raw text if it's not valid JSON
            pass

    return InferenceResponse(
        generated_text=generated_text, safety_attributes=safety_attributes
    )
