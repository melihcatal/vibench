import os

from openai import OpenAI


def alt_text_translate(payload, config=None):
    config = config or {}
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.responses.create(
        model=os.getenv("OPENAI_MODEL", "gpt-5.4-mini"),
        input=[{
            "role": "user",
            "content": f"Translate this image description into {config.get('target_language', 'English')}: {payload.get('description', '')}",
        }],
    )
    return {"translation": response.output_text}
