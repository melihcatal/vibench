import os
from model_client import VertexAIModelClient
from model_models import InferenceRequest, InferenceResponse


def summarize_text(request: InferenceRequest) -> InferenceResponse:
    """Calls a hosted LLM to summarize long text."""
    client = VertexAIModelClient(
        model_name="gemini-pro"
    )  # Using google.cloud.aiplatform via VertexAIModelClient

    prompt = f"Summarize the following text:\n\n{request.prompt}"

    response = client.generate_text(
        prompt,
        max_output_tokens=request.max_output_tokens,
        temperature=request.temperature,
        top_p=request.top_p,
        top_k=request.top_k,
    )

    # Assuming the response has a 'text' attribute or similar based on the client's return type
    # Vertex AI GenerativeModel.generate_content returns a GenerationResponse object
    # with a candidates attribute which is a list of Candidate objects, each having a content.text

    generated_text = ""
    safety_attributes = None

    if response.candidates:
        generated_text = response.candidates[0].content.parts[0].text
        # Safety attributes are usually in response.prompt_feedback or candidate.safety_ratings
        # For simplicity, I'll extract some basic info if available, or keep it None
        safety_attributes = {
            "safety_ratings": [
                sr.to_dict() for sr in response.candidates[0].safety_ratings
            ]
        }

    return InferenceResponse(
        generated_text=generated_text, safety_attributes=safety_attributes
    )
