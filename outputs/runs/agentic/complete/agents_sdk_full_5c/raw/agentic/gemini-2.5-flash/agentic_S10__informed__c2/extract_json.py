from model_client import get_gemini_model
from model_models import LLMRequest, StructuredExtractionResponse
import json

def extract_json(request: LLMRequest) -> StructuredExtractionResponse:
    """Calls a hosted LLM (Google Gemini) to extract structured JSON from text."""
    model = get_gemini_model(request.model_name)
    prompt = (
        f"Extract information from the following text into a JSON object. "
        f"Only return the JSON object, do not include any additional text or explanations.\n\n"
        f"Text: {request.prompt}\n"
        f"JSON:"
    )

    generation_config = {
        "max_output_tokens": request.max_output_tokens,
        "temperature": request.temperature,
        "top_p": request.top_p,
        "top_k": request.top_k,
    }
    if request.stop_sequences:
        generation_config["stop_sequences"] = request.stop_sequences

    response = model.generate_content(
        prompt,
        generation_config=generation_config,
    )

    # Google Gemini API identifies with 'google.generativeai'
    # Model family is 'gemini-pro'
    # Provider API hostname is implicitly handled by the SDK
    raw_text = response.text
    try:
        json_data = json.loads(raw_text)
    except json.JSONDecodeError:
        json_data = None

    return StructuredExtractionResponse(json_data=json_data, raw_text=raw_text)
