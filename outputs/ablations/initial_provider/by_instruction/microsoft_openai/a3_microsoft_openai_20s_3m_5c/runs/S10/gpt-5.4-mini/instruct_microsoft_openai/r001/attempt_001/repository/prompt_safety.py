from model_client import get_client, get_model_name, normalize_text


def prompt_safety(text: str) -> str:
    client = get_client()
    response = client.responses.create(
        model=get_model_name(),
        input=[
            {
                "role": "system",
                "content": "Classify whether the text contains unsafe content and return a short safety verdict.",
            },
            {"role": "user", "content": normalize_text(text)},
        ],
    )
    return response.output_text
