from model_client import get_client, get_model_name, normalize_text


def extract_json(text: str) -> str:
    client = get_client()
    response = client.responses.create(
        model=get_model_name(),
        input=[
            {
                "role": "system",
                "content": "Extract structured JSON from the text and return only valid JSON.",
            },
            {"role": "user", "content": normalize_text(text)},
        ],
    )
    return response.output_text
