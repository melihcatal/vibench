import os
from typing import List, Tuple
from anthropic import Anthropic

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def quality_summary(pairs: List[Tuple[str, str]]) -> str:
    prompt = "Summarize translation quality issues (accuracy, fluency, omissions, etc.) for these pairs:\\n\\n"
    for original, translated in pairs:
        prompt += f"Original: {original}\\nTranslated: {translated}\\n\\n"
    message = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=400,
        temperature=0.1,
        messages=[{"role": "user", "content": prompt}]
    )
    return message.content[0].text