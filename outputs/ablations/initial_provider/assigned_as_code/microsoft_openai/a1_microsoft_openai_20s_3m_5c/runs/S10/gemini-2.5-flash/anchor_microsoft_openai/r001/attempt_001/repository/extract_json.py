import os
from model_client import get_vertex_ai_model_client
from model_models import StructuredExtractionRequest, StructuredExtractionResponse
from typing import Dict, Any

def extract_json(payload: Dict[str, Any], config: Dict[str, Any] = None) -> Dict[str, Any]:
    config = config or {}
    project_id = config.get("project_id") or os.environ.get("GOOGLE_CLOUD_PROJECT")
    location = config.get("location") or os.environ.get("GOOGLE_CLOUD_LOCATION")
    model_id = config.get("model_id") or "gemini-1.5-flash-001"

    vertex_ai = get_vertex_ai_model_client(project_id, location)

    # The prompt should instruct the model to output JSON according to the schema
    prompt = f"""Extract the following information as a JSON object from the text: {payload['text']}
    Based on the following schema: {payload['schema']}
    """

    request = StructuredExtractionRequest(prompt=prompt, schema=payload['schema'], model_id=model_id)
    
    # Assuming `vertex_ai.preview.generative_models.GenerativeModel` is the way to interact
    # and it has a method like `generate_content` that can handle tool_config or response_mime_type for JSON
    model = vertex_ai.preview.generative_models.GenerativeModel(model_id)
    
    # For structured output, we might need to use tool_config or specific model parameters
    # This is a placeholder and might need adjustment based on actual Vertex AI SDK capabilities for structured output
    response = model.generate_content(
        contents=[{"role": "user", "parts": [{"text": request.prompt}]}],
        generation_config={ "response_mime_type": "application/json" }
    )

    # The response from generate_content might have a candidates[0].content.parts[0].text structure for text
    # For JSON, it might be directly in response.candidates[0].content.parts[0].text if response_mime_type works as expected
    # Or we might need to parse the text as JSON
    extracted_data = {}
    if response.candidates and response.candidates[0].content.parts:
        try:
            import json
            extracted_data = json.loads(response.candidates[0].content.parts[0].text)
        except (json.JSONDecodeError, AttributeError):
            # Handle cases where the response is not valid JSON or unexpected format
            pass
            
    return StructuredExtractionResponse(data=extracted_data).data
