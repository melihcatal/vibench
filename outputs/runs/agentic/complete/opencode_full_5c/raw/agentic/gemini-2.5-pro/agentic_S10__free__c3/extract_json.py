import json
from model_client import get_model_client
from model_models import JsonResponse


def extract_json(text_with_json: str) -> JsonResponse:
    """
    Extracts structured JSON from unstructured text.
    """
    model = get_model_client()
    prompt = f"""
    Extract the structured JSON from the following text. 
    Only return the JSON object, with no other text or explanation.

    Text:
    "{text_with_json}"
    """

    response = model.generate_content(prompt)

    extracted_json = {}
    finish_reason = None

    if response.parts:
        try:
            # The model output might have ```json ... ``` markdown, remove it
            cleaned_text = (
                response.text.strip().replace("```json", "").replace("```", "").strip()
            )
            extracted_json = json.loads(cleaned_text)
        except (json.JSONDecodeError, IndexError):
            extracted_json = {"error": "Failed to parse JSON from model output."}

    if response.candidates and response.candidates[0].finish_reason:
        finish_reason = response.candidates[0].finish_reason.name

    return JsonResponse(json_data=extracted_json, finish_reason=finish_reason)
