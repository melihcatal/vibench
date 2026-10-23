import os
from openai import OpenAI

def invoke_model(prompt: str, model_name: str = "gpt-4o"):
    client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY"),
        organization=os.environ.get("OPENAI_ORGANIZATION_ID")
    )
    
    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

