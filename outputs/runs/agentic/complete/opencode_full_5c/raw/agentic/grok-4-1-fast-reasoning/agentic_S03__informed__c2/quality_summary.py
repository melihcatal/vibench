import os
from anthropic import Anthropic, MessageParam


def summarize_translation_quality(
    original_text: str, translated_text: str, source_lang: str, target_lang: str
) -> str:
    client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    prompt = f"""You are a translation quality expert. Analyze the following translation:

Source language: {source_lang}
Original text: {original_text}

Target language: {target_lang}
Translated text: {translated_text}

Provide a concise summary of quality issues (e.g., accuracy, fluency, cultural appropriateness, omissions). If the translation is excellent, state that clearly. Limit to 3-5 sentences."""
    message = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=500,
        temperature=0.1,
        messages=[{"role": "user", "content": prompt}],
    )
    return message.content[0].text
