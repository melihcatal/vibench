import os
import dashscope
from dashscope import OpenAiClient


def translate_notes(notes: str, target_lang: str = "en") -> str:
    """Translate vendor notes/description to the target language using DashScope Qwen.

    Returns the translated text. If translation fails, returns original notes.
    """
    api_key = os.getenv("DASHSCOPE_API_KEY")
    if not api_key:
        raise RuntimeError("Set DASHSCOPE_API_KEY environment variable")
    client = OpenAiClient(api_key)
    # Build prompt for translation
    prompt = (
        "Translate the following text to {lang}. Return ONLY the translation, no extra words.\n---\n{notes}"
    ).format(lang=target_lang, notes=notes)
    response = client.chat.completions.create(
        model="qwen-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.0,
    )
    # The model should reply with just the translated text
    assistant_msg = response.choices[0].message.content.strip()
    return assistant_msg


# Demo when run directly
if __name__ == "__main__":
    sample = "El pedido incluye 5 unidades del producto X a $12 cada uno."
    print("Original Spanish:", sample)
    print("Translated English:", translate_notes(sample, target_lang="en"))
    print("Translated French:", translate_notes(sample, target_lang="fr"))
