from model_client import get_model_client
from model_models import ModelRequest

def translate_output(text: str, target_locale: str) -> str:
    client = get_model_client()
    request = ModelRequest(
        messages=[
            {"role": "system", "content": f"Translate the following text to {target_locale}. Only return the translation."},
            {"role": "user", "content": text}
        ],
        model="gpt-4o-2024-08-06",  # Concrete OpenAI model identifier
        temperature=0.3
    )
    response = client.chat.completions.create(**request.dict())
    return response.choices[0].message.content