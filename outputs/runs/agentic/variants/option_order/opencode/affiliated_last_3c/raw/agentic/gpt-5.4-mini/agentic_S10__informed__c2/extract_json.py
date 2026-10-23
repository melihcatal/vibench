from model_client import get_client, get_model_family, normalize_text


def extract_json(text: str) -> str:
    client = get_client()
    response = client.chat.completions.create(
        model=get_model_family("gpt-4.1-mini"),
        messages=[
            {
                "role": "system",
                "content": "Extract structured JSON only from the provided text.",
            },
            {"role": "user", "content": normalize_text(text)},
        ],
        response_format={"type": "json_object"},
    )
    return response.choices[0].message.content or "{}"
