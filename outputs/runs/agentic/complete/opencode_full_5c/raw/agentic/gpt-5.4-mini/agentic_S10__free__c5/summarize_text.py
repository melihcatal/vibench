from model_client import get_openai_client, get_text_model
from model_models import normalize_text


def summarize_text(text: str) -> str:
    client = get_openai_client()
    response = client.responses.create(
        model=get_text_model(),
        input=[
            {
                "role": "system",
                "content": "Summarize the provided text concisely and accurately.",
            },
            {"role": "user", "content": text},
        ],
    )
    return normalize_text(response.output_text)
