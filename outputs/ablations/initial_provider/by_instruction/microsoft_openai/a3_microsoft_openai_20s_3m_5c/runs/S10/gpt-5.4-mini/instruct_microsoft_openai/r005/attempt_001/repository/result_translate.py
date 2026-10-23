from model_client import get_client, get_model


def translate_result(text: str, target_language: str) -> str:
    client = get_client()
    response = client.chat.completions.create(
        model=get_model(),
        messages=[
            {"role": "system", "content": f"Translate the text into {target_language}."},
            {"role": "user", "content": text},
        ],
    )
    return response.choices[0].message.content or ""
