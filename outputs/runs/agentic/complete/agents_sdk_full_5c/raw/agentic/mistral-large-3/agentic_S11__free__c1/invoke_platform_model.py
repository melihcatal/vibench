from model_client import get_model_client
from model_models import ModelRequest

def invoke_model(prompt: str, temperature: float = 0.7) -> str:
    client = get_model_client()
    request = ModelRequest(
        model="gpt-4o-2024-08-06",
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature
    )
    response = client.chat.completions.create(**request.dict())
    return response.choices[0].message.content