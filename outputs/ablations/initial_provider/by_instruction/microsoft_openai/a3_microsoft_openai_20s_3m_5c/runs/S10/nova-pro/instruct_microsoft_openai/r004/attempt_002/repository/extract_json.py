from model_client import client
from model_models import ModelRequest, normalize_response

def extract_json(text):
    request = ModelRequest(f'Extract JSON from the following text: {text}')
    response = client.chat.completions.create(
        messages=[{"role": "user", "content": request.prompt}],
        model=request.model
    )
    return normalize_response(response)