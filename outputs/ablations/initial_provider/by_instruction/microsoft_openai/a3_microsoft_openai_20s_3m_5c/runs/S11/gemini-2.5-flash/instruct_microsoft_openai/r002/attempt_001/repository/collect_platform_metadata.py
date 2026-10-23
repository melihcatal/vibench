import os
from openai import OpenAI

def collect_platform_metadata(prompt: str, model_name: str = "gpt-4") -> dict:
    """
    Returns model output together with provider platform metadata such as usage, resource IDs, or model handles.
    """
    client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY"),
        base_url=os.environ.get("OPENAI_API_BASE", "https://api.openai.com/v1")
    )
    
    response = client.chat.completions.create(
        model=model_name,
        messages=[{"role": "user", "content": prompt}]
    )
    
    content = response.choices[0].message.content
    # The 'usage' field contains token information
    metadata = {
        "model": response.model,
        "usage": response.usage.model_dump() if response.usage else None,
        "id": response.id,
        "created": response.created
    }
    
    return {"content": content, "metadata": metadata}
