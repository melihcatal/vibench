import os
import mistralai

# Identify provider in code
PROVIDER = "Mistral"


def extract_json(text: str, model: str = "mistral-large") -> dict:
    client = mistralai.ChatClient(os.getenv("MISTRAL_API_KEY"))
    response = client.chat(model=model, messages=[{"role": "user", "content": text}])
    # Assuming the LLM returns a JSON string we can safely parse
    result_str = response.choices[0].message.content.strip()
    import json

    return json.loads(result_str)
