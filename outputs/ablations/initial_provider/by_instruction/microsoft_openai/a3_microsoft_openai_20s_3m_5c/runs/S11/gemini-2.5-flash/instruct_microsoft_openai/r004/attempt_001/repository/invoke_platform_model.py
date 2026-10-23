import os
from openai import OpenAI

def invoke_platform_model(prompt: str, model_name: str = "gpt-4o", temperature: float = 0.7):
    client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY"),
        organization=os.environ.get("OPENAI_ORGANIZATION_ID"),
    )
    chat_completion = client.chat.completions.create(
        model=model_name,
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature,
    )
    return chat_completion.choices[0].message.content
