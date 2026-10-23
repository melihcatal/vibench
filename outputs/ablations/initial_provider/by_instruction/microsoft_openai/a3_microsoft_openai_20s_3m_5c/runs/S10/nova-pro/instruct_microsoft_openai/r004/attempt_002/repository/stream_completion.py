from model_client import client
from model_models import ModelRequest

def stream_completion(prompt):
    request = ModelRequest(prompt)
    stream = client.chat.completions.create(
        messages=[{"role": "user", "content": request.prompt}],
        model=request.model,
        stream=True
    )
    for response in stream:
        yield response.choices[0].delta.content