from model_client import LLMClientFactory
from model_models import LLMRequest, ExtractedJSONResponse
import json
import os

def extract_json(request: LLMRequest) -> ExtractedJSONResponse:
    client = LLMClientFactory.get_anthropic_client()

    model_id = request.model_id if request.model_id else "claude-3-opus-20240229"

    system_prompt = (
        "You are an expert at extracting structured JSON data from text. "
        "Your response must be a valid JSON object. Do not include any prose or explanation."
    )

    messages = [
        {"role": "user", "content": f"{request.prompt}\n\nPlease extract relevant information as a JSON object."}
    ]

    response = client.messages.create(
        model=model_id,
        max_tokens=request.max_tokens,
        temperature=request.temperature,
        system=system_prompt,
        messages=messages,
        **request.kwargs
    )

    response_text = response.content[0].text
    try:
        extracted_json = json.loads(response_text)
    except json.JSONDecodeError:
        extracted_json = {"error": "Failed to parse JSON from LLM response", "raw_response": response_text}

    return ExtractedJSONResponse(json_content=extracted_json, model_id=model_id, raw_text=response_text)