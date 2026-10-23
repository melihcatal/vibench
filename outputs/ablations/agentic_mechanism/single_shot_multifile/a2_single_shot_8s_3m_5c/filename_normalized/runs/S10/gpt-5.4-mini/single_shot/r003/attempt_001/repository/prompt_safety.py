from openai import OpenAI
from model_client import get_text_client, resolve_text_model
from model_models import normalize_text_result


def prompt_safety(prompt: str, generated_text: str = "", model: str | None = None) -> str:
    client = get_text_client()
    model_name = resolve_text_model(model, task="safety")
    content = f"Analyze the following user prompt and generated text for unsafe content, policy violations, and disallowed requests. Return a concise safety assessment.\n\nPrompt:\n{prompt}\n\nGenerated text:\n{generated_text}"
    response = client.responses.create(model=model_name, input=content)
    return normalize_text_result(response)
