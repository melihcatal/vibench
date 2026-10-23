from model_client import build_client, load_config
from model_models import safe_context_prompt


def answer_with_context(question: str, context: str, provider: str = "openai") -> str:
    config = load_config(provider=provider)
    client = build_client(config)
    response = client.chat.completions.create(
        model=config.model,
        messages=[{"role": "user", "content": safe_context_prompt(question, context)}],
        temperature=0.2,
    )
    return response.choices[0].message.content or ""
