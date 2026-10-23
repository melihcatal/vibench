from model_client import get_model_client
from model_models import ModelRequest

def stream_model_generation(prompt: str, system_message: str = None):
    client = get_model_client()
    request = ModelRequest(
        messages=[
            {"role": "system", "content": system_message} if system_message else {"role": "user", "content": prompt},
            {"role": "user", "content": prompt}
        ],
        model="gpt-4o-2024-08-06",  # Concrete OpenAI model identifier
        temperature=0.7,
        stream=True
    )
    for chunk in client.chat.completions.create(**request.dict()):
        if chunk.choices[0].delta.content:
            yield chunk