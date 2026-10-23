from typing import List, Tuple
import os
from mistralai.client import MistralClient


def summarize_translation_quality(pairs: List[Tuple[str, str]]) -> str:
    client = MistralClient(api_key=os.getenv("MISTRAL_API_KEY"))
    if not client.api_key:
        raise ValueError("MISTRAL_API_KEY environment variable is required.")
    pair_str = "\n".join(
        [
            f"Original ({len(pairs)}): {orig}\nTranslated: {trans}"
            for orig, trans in pairs
        ]
    )
    prompt = f"""Review the following translation pairs for quality issues including accuracy, fluency, naturalness, cultural appropriateness, omissions, awkward phrasing, or literal translations.

Translation pairs:
{pair_str}

Provide a concise summary of main issues found, or "No significant issues detected" if translations are high quality."""
    chat_response = client.chat.complete(
        model="mistral-large-latest", messages=[{"role": "user", "content": prompt}]
    )
    return chat_response.choices[0].message.content
