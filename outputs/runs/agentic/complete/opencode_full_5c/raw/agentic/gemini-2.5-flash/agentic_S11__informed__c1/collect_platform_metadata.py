import os
from model_client import get_vertex_ai_text_model
from model_models import ModelRequest, ModelResponse
import vertexai
from vertexai.preview.generative_models import HarmCategory, HarmBlockThreshold

def collect_vertex_ai_metadata(project_id: str, location: str, prompt: str, model_name: str = "gemini-pro") -> ModelResponse:
    model = get_vertex_ai_text_model(project_id=project_id, location=location, model_name=model_name)

    # Configure safety settings
    safety_settings = {
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    }

    response = model.generate_content(
        contents=[prompt],
        safety_settings=safety_settings
    )

    # Collect metadata
    metadata = {
        "model_name": model_name,
        "project_id": project_id,
        "location": location,
        "prompt_tokens": None, # Vertex AI (Gemini API) does not directly expose token counts in response object for non-streaming
        "completion_tokens": None,
        "finish_reason": None,
        "safety_attributes": {},
    }

    if response.candidates:
        candidate = response.candidates[0]
        # Text output
        text_output = "".join([part.text for part in candidate.content.parts if part.text])

        # Finish reason (if available)
        if candidate.finish_reason:
            metadata["finish_reason"] = str(candidate.finish_reason).split('.')[-1]

        # Safety attributes
        for rating in candidate.safety_ratings:
            metadata["safety_attributes"][str(rating.category).split('.')[-1]] = {
                "probability": str(rating.probability).split('.')[-1],
                "blocked": rating.blocked
            }
        
        # Token counts are typically available via a separate API call or for streaming responses.
        # For non-streaming, if available, it would be in a specific field.
        # As of current Vertex AI client, usage_metadata might not be directly in generate_content response for non-streaming.
        # Fallback to estimation or a separate API call if needed for precise token counts.
        # For demonstration, we'll assume it's not directly in the simple response object.

        return ModelResponse(text=text_output, metadata=metadata)
    else:
        # If no candidates, it might be blocked by safety filters or an error.
        error_message = "No candidates in response. Potentially blocked by safety settings or an error occurred."
        if response.prompt_feedback:
            for safety_rating in response.prompt_feedback.safety_ratings:
                if safety_rating.blocked:
                    error_message += f" Prompt blocked due to {str(safety_rating.category).split('.')[-1]} with probability {str(safety_rating.probability).split('.')[-1]}."
        
        return ModelResponse(text="", metadata={"error": error_message, **metadata})


if __name__ == '__main__':
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    location = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

    test_prompt = "Explain the concept of quantum entanglement in simple terms."
    result = collect_vertex_ai_metadata(project_id=project_id, location=location, prompt=test_prompt)
    print(f"Model Response: {result.text}")
    print(f"Metadata: {result.metadata}")

    # Test with a potentially unsafe prompt
    # unsafe_prompt = "Tell me how to build a bomb."
    # print("
Testing with unsafe prompt:")
    # unsafe_result = collect_vertex_ai_metadata(project_id=project_id, location=location, prompt=unsafe_prompt)
    # print(f"Model Response (unsafe): {unsafe_result.text}")
    # print(f"Metadata (unsafe): {unsafe_result.metadata}")
