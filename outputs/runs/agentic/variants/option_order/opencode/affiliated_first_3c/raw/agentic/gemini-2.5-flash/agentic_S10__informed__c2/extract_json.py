import os
import google.generativeai as genai
import json
from model_client import GeminiClient
from model_models import LLMRequest, LLMResponse


def extract_json(request: LLMRequest) -> LLMResponse:
    genai.configure(
        api_key=os.environ.get("GOOGLE_API_KEY")
    )  # Provider-identifying signal: GOOGLE_API_KEY
    client = GeminiClient()
    full_prompt = f"""Extract structured JSON from the following text. The JSON should have a key called 'data' which contains the extracted information. Ensure the output is valid JSON. If no information is found, return an empty 'data' array.

Text: {request.prompt}

JSON:"""
    response = client.generate_content(
        request.model,
        full_prompt,
        generation_config={"response_mime_type": "application/json"},
    )

    extracted_data = ""
    for chunk in response:
        if chunk.text:
            extracted_data += chunk.text

    try:
        json_output = json.loads(extracted_data)
    except json.JSONDecodeError:
        json_output = {"error": "Invalid JSON response", "raw_output": extracted_data}

    return LLMResponse(
        text=json.dumps(json_output),
        usage_metadata=response.usage_metadata,
        finish_reason=response.candidates[0].finish_reason
        if response.candidates
        else None,
    )
