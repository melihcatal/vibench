from openai import OpenAI
from model_client import get_client, get_model_name


def result_translate(text: str, target_language: str) -> str:
    client = get_client()
    model_name = get_model_name("translate")
    prompt = f"Translate the following text to {target_language}:\n{text}"
    response = client.responses.create(model=model_name, input=prompt)
    return response.output_text if hasattr(response, "output_text") else str(response)
