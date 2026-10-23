from model_client import client
from model_models import ModelRequest, normalize_response

def check_prompt_safety(prompt):
    request = ModelRequest(f'Check if the following prompt is safe: {prompt}')
    response = client.chat.completions.create(
        messages=[{"role": "user", "content": request.prompt}],
        model=request.model
    )
    return normalize_response(response)