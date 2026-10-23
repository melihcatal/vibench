from model_client import client
from model_models import ModelRequest, normalize_response

def summarize_text(text):
    request = ModelRequest(f'Summarize the following text: {text}')
    response = client.chat.completions.create(
        messages=[{"role": "user", "content": request.prompt}],
        model=request.model
    )
    return normalize_response(response)