from model_client import client
from model_models import ModelRequest, normalize_response

def generate_spoken_brief(text):
    request = ModelRequest(f'Generate a spoken brief from the following text: {text}')
    response = client.chat.completions.create(
        messages=[{"role": "user", "content": request.prompt}],
        model=request.model
    )
    return normalize_response(response)