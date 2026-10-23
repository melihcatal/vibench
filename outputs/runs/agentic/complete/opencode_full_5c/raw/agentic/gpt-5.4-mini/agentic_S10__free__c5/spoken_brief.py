from model_client import get_openai_client, get_text_model
from model_models import normalize_text


def spoken_brief(text: str) -> str:
    client = get_openai_client()
    response = client.responses.create(
        model=get_text_model(),
        input=[
            {
                "role": "system",
                "content": "Rewrite the content as a short spoken brief suitable for audio narration.",
            },
            {"role": "user", "content": text},
        ],
    )
    return normalize_text(response.output_text)
