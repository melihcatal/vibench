import os
from openai import OpenAI

def localized_platform_output(text: str, target_language: str = "French"):
    client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY"),
        organization=os.environ.get("OPENAI_ORGANIZATION_ID"),
    )
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": f"Translate the following text into {target_language}."},
            {"role": "user", "content": text}
        ]
    )
    return response.choices[0].message.content
