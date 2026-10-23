import google.generativeai as genai
import json
from model_client import GeminiClient
from model_models import StructuredExtractionRequest, LLMResponse


def extract_json(request: StructuredExtractionRequest) -> LLMResponse:
    client = GeminiClient.get_client()
    prompt = f"Extract information from the following text into a JSON object conforming to this schema:\n{json.dumps(request.schema, indent=2)}\n\nText:\n{request.text}\n\nJSON:"

    config = {
        "temperature": request.temperature,
        "response_mime_type": "application/json",
    }

    # The Gemini API might not directly enforce schema, so we guide it with the prompt
    # and expect it to return valid JSON which we then parse.

    response = client.generate_content(prompt, generation_config=config)

    # Attempt to parse the text as JSON. If it fails, return the raw text.
    try:
        parsed_json = json.loads(response.text)
        return LLMResponse(
            text=json.dumps(
                parsed_json, indent=2
            ),  # Re-serialize for consistent formatting
            finish_reason=response.candidates[0].finish_reason.name
            if response.candidates
            else None,
            usage_metadata=None,
        )
    except json.JSONDecodeError:
        return LLMResponse(
            text=response.text,
            finish_reason=response.candidates[0].finish_reason.name
            if response.candidates
            else None,
            usage_metadata=None,
        )
