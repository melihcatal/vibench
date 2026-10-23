import os
from openai import OpenAI

def collect_platform_metadata(prompt: str, model_name: str = "gpt-4o"):
    client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY"),
        organization=os.environ.get("OPENAI_ORGANIZATION_ID"),
    )
    response = client.chat.completions.create(
        model=model_name,
        messages=[{"role": "user", "content": prompt}]
    )
    
    content = response.choices[0].message.content
    metadata = {
        "id": response.id,
        "model": response.model,
        "usage": response.usage.model_dump() if response.usage else None,
        "finish_reason": response.choices[0].finish_reason
    }
    return {"content": content, "metadata": metadata}
