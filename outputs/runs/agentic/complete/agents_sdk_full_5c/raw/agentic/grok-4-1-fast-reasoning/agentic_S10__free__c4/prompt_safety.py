import os
from openai import OpenAI
from typing import Optional

def check_prompt_safety(prompt: str, generated_text: Optional[str] = None) -> bool:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    texts = [prompt]
    if generated_text:
        texts.append(generated_text)
    for text in texts:
        moderation = client.moderations.create(
            input=text,
            model="text-moderation-latest",
        )
        if moderation.results[0].flagged:
            return False
    return True
