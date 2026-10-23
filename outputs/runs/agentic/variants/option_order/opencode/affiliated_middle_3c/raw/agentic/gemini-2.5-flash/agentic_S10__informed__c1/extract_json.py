from model_client import get_gemini_client
from model_models import LLMRequest, LLMResponse, normalize_json_output


def extract_json(request: LLMRequest) -> LLMResponse:
    model = get_gemini_client()
    prompt = (
        f"Please extract structured JSON data from the following text. "
        f"The JSON should represent the key entities and their attributes.\n\n{request.prompt}\n\n"
        f"Please respond with only the JSON object."
    )
    response = model.generate_content(
        prompt,
        generation_config={
            "temperature": request.temperature,
            "max_output_tokens": request.max_tokens,
        },
    )

    # The model might return text along with JSON, so we need to parse it.
    extracted_data = normalize_json_output(response.text)
    return LLMResponse(text=str(extracted_data), model=request.model)
