import os
from model_client import get_client
from model_models import PlatformRequest, normalize_text

def invoke_platform_model(prompt: str):
    client = get_client()
    req = PlatformRequest(prompt=prompt)
    response = client.chat.completions.create(model=os.getenv('OPENAI_MODEL', 'gpt-4.1-mini'), messages=[{'role': 'user', 'content': req.prompt}])
    return normalize_text(response.choices[0].message.content)
