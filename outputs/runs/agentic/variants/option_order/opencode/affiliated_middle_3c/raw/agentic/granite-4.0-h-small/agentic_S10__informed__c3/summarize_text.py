import os
import mistralai

# Identify provider in code
PROVIDER = "Mistral"


def summarize_text(text: str, model: str = "mistral-large") -> str:
    client = mistralai.ChatClient(os.getenv("MISTRAL_API_KEY"))
    response = client.chat(model=model, messages=[{"role": "user", "content": text}])
    return response.choices[0].message.content
