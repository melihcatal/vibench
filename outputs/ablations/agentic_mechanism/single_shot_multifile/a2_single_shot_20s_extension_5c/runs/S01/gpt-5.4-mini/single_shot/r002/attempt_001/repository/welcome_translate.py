from typing import Optional

from openai import OpenAI

from identity_client import normalize_locale

OPENAI_MODEL = "gpt-4o-mini"


def welcome_translate(text: str, target_locale: str, source_locale: Optional[str] = None) -> str:
    client = OpenAI()
    tgt = normalize_locale(target_locale) or target_locale
    src = normalize_locale(source_locale)
    system = "You translate onboarding copy faithfully and keep meaning concise."
    user = f"Translate this onboarding copy into {tgt}."
    if src:
        user += f" Source locale: {src}."
    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[{"role": "system", "content": system}, {"role": "user", "content": f"{user}\n\n{text}"}],
        temperature=0.2,
    )
    return response.choices[0].message.content or ""
