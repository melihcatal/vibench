from model_client import get_openai_client, get_text_model
from model_models import normalize_json_text


def extract_json(text: str) -> dict:
    client = get_openai_client()
    response = client.responses.create(
        model=get_text_model(),
        input=[
            {
                "role": "system",
                "content": "Extract the requested data and return only valid JSON.",
            },
            {"role": "user", "content": text},
        ],
    )
    return normalize_json_text(response.output_text)
