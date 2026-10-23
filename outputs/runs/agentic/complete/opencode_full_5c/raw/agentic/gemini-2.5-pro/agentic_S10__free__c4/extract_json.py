import json
from model_client import get_openai_client
from model_models import JSONModelResponse


def extract_json(text_with_json: str) -> JSONModelResponse:
    client = get_openai_client()
    response = client.chat.completions.create(
        model="gpt-4o",
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that extracts JSON from text. Output only valid JSON.",
            },
            {
                "role": "user",
                "content": f"Extract the JSON object from this text: {text_with_json}",
            },
        ],
    )
    choice = response.choices[0]
    try:
        json_object = json.loads(choice.message.content)
    except json.JSONDecodeError:
        json_object = {}

    return JSONModelResponse(
        json_object=json_object,
        model=response.model,
        usage=dict(response.usage),
    )
