import os
import anthropic
from typing import str


def quality_summary(original_text: str, translated_text: str) -> str:
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    prompt = f"""You are a translation quality expert. Analyze the following translation:

Original: {original_text}

Translated: {translated_text}

Summarize quality issues in bullet points covering accuracy, fluency, completeness, tone. If no issues, state "High quality translation with no significant issues." """

    message = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=400,
        temperature=0.3,
        messages=[{"role": "user", "content": prompt}],
    )
    return message.content[0].text
