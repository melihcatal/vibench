import os
import json
from model_client import vertex_client
from model_models import LLMRequest, LLMResponse


def extract_json_from_text(
    text: str, json_schema: dict, model_name: str = "gemini-pro"
) -> LLMResponse:
    """
    Calls a hosted LLM (Vertex AI's Gemini Pro) to extract structured JSON from text
    according to a provided schema.
    """
    prompt = f"""
    Extract information from the following text into a JSON object that conforms to the provided JSON schema.
    Only return the JSON object.

    Text:
    {text}

    JSON Schema:
    {json.dumps(json_schema, indent=2)}
    """

    # Use the shared client
    extracted_content = vertex_client.generate_content(
        model_name=model_name,
        prompt=prompt,
        temperature=0.1,  # Low temperature for structured output
        max_output_tokens=1024,
    )

    # Attempt to parse the JSON output
    try:
        parsed_json = json.loads(extracted_content)
        return LLMResponse(
            text=json.dumps(parsed_json, indent=2),
            metadata={
                "model_provider": "google_vertex_ai",
                "model_name": model_name,
                "parsed_successfully": True,
            },
        )
    except json.JSONDecodeError:
        return LLMResponse(
            text=extracted_content,
            metadata={
                "model_provider": "google_vertex_ai",
                "model_name": model_name,
                "parsed_successfully": False,
                "error": "JSON decoding failed",
            },
        )
