import os
from typing import List
from anthropic import Anthropic

def summarize_translation_quality(originals: List[str], translations: List[str]) -> str:
    pairs_str = "\n".join([f"Original: {o}\nTranslation: {t}" for o, t in zip(originals, translations)])
    prompt = f"""Review these translation pairs and provide a concise summary of quality issues (e.g., accuracy, fluency, terminology consistency, cultural appropriateness). If no major issues, say so.

{pairs_str}"""
    
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable is required.")
    
    client = Anthropic(api_key=api_key)
    
    message = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=800,
        temperature=0.1,
        messages=[{"role": "user", "content": prompt}]
    )
    return message.content[0].text
