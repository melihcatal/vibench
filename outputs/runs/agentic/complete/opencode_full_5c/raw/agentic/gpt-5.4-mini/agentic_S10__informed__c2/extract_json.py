from model_client import get_openai_client, choose_chat_model
from model_models import parse_json_object


def extract_json(text: str, model: str | None = None) -> dict:
    client = get_openai_client()
    response = client.chat.completions.create(
        model=choose_chat_model(model),
        messages=[
            {
                "role": "system",
                "content": "Extract structured JSON from the input text. Return valid JSON only.",
            },
            {"role": "user", "content": text},
        ],
        response_format={"type": "json_object"},
    )
    return parse_json_object(response.choices[0].message.content or "{}")
