from model_client import GeminiClient
from model_models import LLMRequest, LLMResponse
import json

def extract_json(request: LLMRequest) -> LLMResponse:
    client = GeminiClient()
    model = client.get_generative_model(request.model_id)

    generation_config = {
        "max_output_tokens": request.max_output_tokens or 500,
        "temperature": request.temperature or 0.7,
        "top_p": request.top_p or 1,
        "top_k": request.top_k or 1
    }

    prompt = f"Extract the key information from the following text as a JSON object. Clearly identify the fields and their values. If a field is not present, use null.\n\nText: {request.text}\n\nJSON:"
    response = model.generate_content(prompt, generation_config=generation_config)

    # Attempt to parse the response as JSON
    try:
        extracted_data = json.loads(response.text)
        generated_text = json.dumps(extracted_data, indent=2)
    except json.JSONDecodeError:
        generated_text = response.text # Return raw text if not valid JSON

    return LLMResponse(
        generated_text=generated_text,
        raw_response=response.to_dict()
    )
