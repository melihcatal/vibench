import os
from model_client import get_client
from model_models import PlatformRequest, PlatformResult

def collect_platform_metadata(prompt: str):
    client = get_client()
    req = PlatformRequest(prompt=prompt)
    response = client.chat.completions.create(model=os.getenv('OPENAI_MODEL', 'gpt-4.1-mini'), messages=[{'role': 'user', 'content': req.prompt}])
    choice = response.choices[0].message.content
    usage = getattr(response, 'usage', None)
    return PlatformResult(text=choice, model=os.getenv('OPENAI_MODEL', 'gpt-4.1-mini'), usage=usage, raw=response)
