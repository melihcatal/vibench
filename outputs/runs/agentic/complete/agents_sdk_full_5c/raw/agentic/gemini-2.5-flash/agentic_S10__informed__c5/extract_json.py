from model_client import LLMClient
from model_models import LLMRequest, LLMResponse
import json

def extract_json(text: str, json_schema: str) -> LLMResponse:
    """Calls a hosted LLM to extract structured JSON from text."""
    llm_client = LLMClient().get_client()
    model = llm_client.GenerativeModel('gemini-pro')

    prompt = (
        f"Extract information from the following text into a JSON object "
        f"that conforms to this JSON schema:\n\n{json_schema}\n\n"
        f"Text to extract from:\n\n{text}\n\n"
        f"Ensure the output is only the JSON object."
    )

    response = model.generate_content(
        prompt,
        generation_config={
            "temperature": 0.1,
            "response_mime_type": "application/json"
        }
    )
    try:
        json_output = json.loads(response.text)
        return LLMResponse(json_output=json_output, raw_response=response)
    except json.JSONDecodeError:
        return LLMResponse(text=response.text, raw_response=response)
