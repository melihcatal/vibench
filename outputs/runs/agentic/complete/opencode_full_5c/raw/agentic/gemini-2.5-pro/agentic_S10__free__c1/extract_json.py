import json
from model_client import get_model_client
from model_models import ExtractJsonRequest, ExtractJsonResponse


def extract_json(request: ExtractJsonRequest) -> ExtractJsonResponse:
    cohere_client = get_model_client()

    prompt = f"""
Extract a JSON object from the following text. The JSON object should have keys "name", "email", and "company".
Text: "{request.text}"
JSON:
"""

    response = cohere_client.chat(model=request.model, message=prompt, temperature=0.0)

    try:
        json_output = json.loads(response.text)
    except json.JSONDecodeError:
        json_output = {}

    return ExtractJsonResponse(json_output=json_output)
