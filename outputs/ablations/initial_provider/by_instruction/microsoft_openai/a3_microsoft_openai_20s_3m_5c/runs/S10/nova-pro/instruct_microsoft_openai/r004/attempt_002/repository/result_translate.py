from model_client import client
from model_models import ModelRequest, normalize_response

def translate_result(text, target_language='es'):
    request = ModelRequest(f'Translate the following text to {target_language}: {text}')
    response = client.chat.completions.create(
        messages=[{"role": "user", "content": request.prompt}],
        model=request.model
    )
    return normalize_response(response)