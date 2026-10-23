from openai import OpenAI

from model_client import get_openai_client, select_chat_model
from model_models import GenerationRequest, ensure_json_schema_name, usage_to_dict


def extract_json(
    text: str,
    json_schema: dict,
    schema_name: str = "extracted_payload",
    model: str | None = None,
) -> dict:
    client: OpenAI = get_openai_client()
    selected_model = select_chat_model(task="json", preferred_model=model)
    response = client.responses.create(
        model=selected_model,
        input=[
            {
                "role": "system",
                "content": [
                    {
                        "type": "input_text",
                        "text": "Extract the requested information from the text and return strictly valid JSON matching the schema.",
                    }
                ],
            },
            {
                "role": "user",
                "content": [{"type": "input_text", "text": text}],
            },
        ],
        text={
            "format": {
                "type": "json_schema",
                "name": ensure_json_schema_name(schema_name),
                "schema": json_schema,
                "strict": True,
            }
        },
    )
    return {
        "provider": "OpenAI",
        "model": response.model,
        "json_text": response.output_text,
        "usage": usage_to_dict(response.usage),
    }
