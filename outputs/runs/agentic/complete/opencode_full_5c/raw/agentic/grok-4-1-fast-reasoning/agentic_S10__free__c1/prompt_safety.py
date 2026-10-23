import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def is_prompt_safe(prompt: str) -> bool:
    \"\"\"Check prompt for unsafe content using OpenAI moderation API.\"\"\"
    response = client.moderations.create(
        input=prompt,
        model="text-moderation-3.5-moderate"
    )
    result = response.results[0]
    return not result.flagged

def is_text_safe(text: str) -> bool:
    \"\"\"Check generated text for unsafe content.\"\"\"
    return is_prompt_safe(text)