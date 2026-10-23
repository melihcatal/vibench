from model_client import get_openai_client, get_model_family
from model_models import normalize_text


def check_prompt_safety(prompt: str) -> str:
    client = get_openai_client()
    response = client.responses.create(
        model=get_model_family(),
        input=[
            {
                "role": "system",
                "content": "Classify the safety of the text and return SAFE or UNSAFE with a short reason.",
            },
            {"role": "user", "content": prompt},
        ],
    )
    return normalize_text(response.output_text)


def check_generated_text_safety(text: str) -> str:
    return check_prompt_safety(text)
