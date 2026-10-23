from openai import OpenAI
from model_client import get_client, get_model_name


def prompt_safety(prompt: str, generated_text: str = "") -> dict:
    client = get_client()
    model_name = get_model_name("safety")
    content = f"Prompt:\n{prompt}\n\nGenerated text:\n{generated_text}"
    response = client.responses.create(model=model_name, input=content)
    text = response.output_text if hasattr(response, "output_text") else str(response)
    return {"model": model_name, "assessment": text}
