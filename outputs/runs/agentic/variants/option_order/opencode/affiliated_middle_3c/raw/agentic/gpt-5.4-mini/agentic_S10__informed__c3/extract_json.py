from model_client import get_client, get_model_name


def extract_json(text: str) -> str:
    client = get_client()
    response = client.chat.completions.create(
        model=get_model_name(),
        messages=[
            {
                "role": "system",
                "content": "Extract the requested structure as valid JSON only.",
            },
            {"role": "user", "content": text},
        ],
    )
    return response.choices[0].message.content or "{}"
