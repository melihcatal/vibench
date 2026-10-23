from openai import OpenAI
import os

def collect_model_metadata(prompt: str, model_name: str = "gpt-4o"):
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model=model_name,
        messages=[{"role": "user", "content": prompt}]
    )
    return {
        "output": response.choices[0].message.content,
        "usage": response.usage.model_dump(),
        "model_id": response.model
    }
