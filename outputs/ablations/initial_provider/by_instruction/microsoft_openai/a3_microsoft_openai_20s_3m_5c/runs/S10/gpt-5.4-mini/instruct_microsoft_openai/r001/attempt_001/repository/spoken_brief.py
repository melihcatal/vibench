from model_client import get_client, get_model_name, normalize_text


def spoken_brief(text: str) -> str:
    client = get_client()
    response = client.responses.create(
        model=get_model_name(),
        input=[
            {
                "role": "system",
                "content": "Generate a short spoken brief that sounds natural when read aloud.",
            },
            {"role": "user", "content": normalize_text(text)},
        ],
    )
    return response.output_text
