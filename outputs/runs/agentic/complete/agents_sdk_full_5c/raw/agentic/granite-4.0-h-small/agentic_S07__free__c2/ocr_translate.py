import openai

def ocr_translate(text: str, target_lang: str = 'es') -> str:
    """Translate extracted OCR text using OpenAI's translation endpoint (ChatGPT)."""
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": f"Translate the following text to {target_lang}:\\n\\n{text}"}],
    )
    return response.choices[0].message.content.strip()
