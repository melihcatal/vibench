import os
import openai
from typing import List


def translate_transcript(segments: List[str], target_lang: str = "es") -> List[str]:
    """Translate completed transcript segments to a target language using OpenAI's ChatGPT model.

    Args:
        segments: List of text chunks (e.g., sentences or paragraphs) from a transcript.
        target_lang: ISO language code for the target language (default Spanish).

    Returns:
        List of translated segment strings.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("Missing OPENAI_API_KEY environment variable")

    client = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": f"You are a professional translator. Translate each input segment into {target_lang} while preserving meaning and punctuation.",
            },
            {
                "role": "user",
                "content": "Translate the following segments:\n"
                + "\n".join(f"> {seg}" for seg in segments),
            },
        ],
    )
    response = client.choices[0].message.content
    # The model outputs each translation prefixed with "Translation:", so extract the text.
    translated = []
    for line in response.splitlines():
        if line.startswith("Translation:"):
            translated.append(line[len("Translation:") :].strip())
    return translated
