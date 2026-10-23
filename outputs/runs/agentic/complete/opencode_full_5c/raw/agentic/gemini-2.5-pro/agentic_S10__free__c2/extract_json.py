import json
from model_client import get_anthropic_client
from model_models import ModelRequest, ModelResponse


def extract_json(request: ModelRequest) -> ModelResponse:
    client = get_anthropic_client()

    if not request.prompt:
        raise ValueError("Prompt for JSON extraction cannot be empty.")

    model = request.model if request.model else "claude-3-sonnet-20240229"

    response = client.messages.create(
        model=model,
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": f"Extract a JSON object from the following text. The JSON object should have keys 'name' and 'details'. Text: {request.prompt}",
            }
        ],
    )

    text_content = response.content[0].text
    try:
        json_str_start = text_content.find("{")
        json_str_end = text_content.rfind("}") + 1
        if json_str_start != -1 and json_str_end != 0:
            json_str = text_content[json_str_start:json_str_end]
            json.loads(json_str)
        else:
            json_str = ""
    except (json.JSONDecodeError, IndexError):
        json_str = ""

    return ModelResponse(text=json_str, raw_response=response)
