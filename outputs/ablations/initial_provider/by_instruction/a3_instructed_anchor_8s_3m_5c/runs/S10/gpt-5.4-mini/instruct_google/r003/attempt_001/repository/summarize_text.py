from model_client import get_client, get_model_config
from model_models import normalize_text


def summarize_text(text: str) -> str:
    client = get_client()
    config = get_model_config()
    prompt = f"Summarize the following text concisely and accurately:\n\n{text}"
    response = client.models.generate_content(
        model=config.model,
        contents=prompt,
        config={
            "temperature": config.temperature,
            "top_p": config.top_p,
            "max_output_tokens": config.max_output_tokens,
        },
    )
    return normalize_text(getattr(response, "text", response))
