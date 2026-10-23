import os
from openai import OpenAI

def collect_platform_metadata(prompt: str, model_name: str = "gpt-4o", temperature: float = 0.7):
    client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY"),
        organization=os.environ.get("OPENAI_ORGANIZATION_ID"),
    )
    chat_completion = client.chat.completions.create(
        model=model_name,
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature,
    )
    content = chat_completion.choices[0].message.content
    metadata = {
        "model": chat_completion.model,
        "id": chat_completion.id,
        "created": chat_completion.created,
        "usage": chat_completion.usage.model_dump() if chat_completion.usage else None,
    }
    return content, metadata
