import os
import mistralai

# Identify provider in code
PROVIDER = "Mistral"


def stream_completion(prompt: str, model: str = "mistral-large"):
    client = mistralai.ChatClient(os.getenv("MISTRAL_API_KEY"))
    # Using stream=True to yield partial tokens
    response = client.chat(
        model=model, messages=[{"role": "user", "content": prompt}], stream=True
    )
    for chunk in response:
        yield chunk.choices[0].delta.content or ""
