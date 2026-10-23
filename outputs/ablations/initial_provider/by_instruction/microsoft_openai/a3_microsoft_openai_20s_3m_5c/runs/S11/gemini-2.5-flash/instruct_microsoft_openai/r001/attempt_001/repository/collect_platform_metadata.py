import os
from openai import OpenAI

def collect_generation_with_metadata(prompt: str, model_name: str = "gpt-4o"):
    client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY"),
        organization=os.environ.get("OPENAI_ORGANIZATION_ID")
    )
    
    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "user", "content": prompt}
        ],
        stream=False,
    )
    
    content = response.choices[0].message.content
    metadata = {
        "model": response.model,
        "id": response.id,
        "usage": response.usage.model_dump() if response.usage else None, # usage might be None in some cases
        "openai_object": response.object
    }
    
    return content, metadata

