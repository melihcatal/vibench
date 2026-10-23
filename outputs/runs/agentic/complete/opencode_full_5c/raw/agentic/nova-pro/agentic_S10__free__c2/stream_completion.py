from model_client import ANTHROPIC_API_URL, ANTHROPIC_API_KEY
from model_models import ModelRequest, ModelResponse


def stream_completion(prompt):
    headers = {
        "Authorization": f"Bearer {ANTHROPIC_API_KEY}",
        "Content-Type": "application/json",
    }
    data = {"prompt": prompt, "max_tokens_to_sample": 100, "stream": True}
    response = requests.post(ANTHROPIC_API_URL, headers=headers, json=data, stream=True)
    for line in response.iter_lines():
        if line:
            yield line.decode("utf-8")
