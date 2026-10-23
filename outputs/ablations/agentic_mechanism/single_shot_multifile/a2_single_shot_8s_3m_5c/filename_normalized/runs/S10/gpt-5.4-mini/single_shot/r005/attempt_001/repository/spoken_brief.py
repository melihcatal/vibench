from openai import OpenAI
from model_client import get_client, get_model_name


def spoken_brief(text: str) -> str:
    client = get_client()
    model_name = get_model_name("spoken")
    prompt = f"Rewrite the following as a short spoken brief suitable for text-to-speech:\n{text}"
    response = client.responses.create(model=model_name, input=prompt)
    return response.output_text if hasattr(response, "output_text") else str(response)
