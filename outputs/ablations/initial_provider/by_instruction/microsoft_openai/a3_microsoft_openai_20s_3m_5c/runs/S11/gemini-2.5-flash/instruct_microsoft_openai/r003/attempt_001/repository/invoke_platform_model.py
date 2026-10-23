from openai import OpenAI
import os

def invoke_model(prompt: str, model_name: str = "gpt-4o"):
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model=model_name,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content
