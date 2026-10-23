from model_client import get_openai_client, get_text_model
from model_models import normalize_text


def translate_result(text: str, target_language: str) -> str:
    client = get_openai_client()
    response = client.responses.create(
        model=get_text_model(),
        input=[
            {
                "role": "system",
                "content": f"Translate the text into {target_language} while preserving meaning.",
            },
            {"role": "user", "content": text},
        ],
    )
    return normalize_text(response.output_text)
