import os
from openai import OpenAI

def invoke_platform_model(prompt: str, model_name: str = "gpt-4"):
    """
    Invokes a provider-managed model through a project-, deployment-,
    or inference-profile-scoped platform client.
    """
    client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY"),
        base_url=os.environ.get("OPENAI_API_BASE", "https://api.openai.com/v1")
    )
    
    response = client.chat.completions.create(
        model=model_name,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content
