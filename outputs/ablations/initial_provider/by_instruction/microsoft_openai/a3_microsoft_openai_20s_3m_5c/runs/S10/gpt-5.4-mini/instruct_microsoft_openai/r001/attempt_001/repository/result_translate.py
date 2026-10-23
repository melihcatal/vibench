from model_client import get_client, get_model_name, normalize_text


def result_translate(text: str, target_language: str) -> str:
    client = get_client()
    response = client.responses.create(
        model=get_model_name(),
        input=[
            {
                "role": "system",
                "content": f"Translate the text into {normalize_text(target_language)}.",
            },
            {"role": "user", "content": normalize_text(text)},
        ],
    )
    return response.output_text
