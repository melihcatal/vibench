import os
from openai import OpenAI


OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
OPENAI_MODEL = "gpt-4o"


def translate_onboarding_copy(
    text: str,
    target_locale: str,
    source_locale: str = "en",
    context: str = "onboarding",
) -> str:
    client = OpenAI(api_key=OPENAI_API_KEY)

    system_prompt = (
        f"You are a professional translator specializing in software onboarding content. "
        f"Translate the following text from {source_locale} to {target_locale}. "
        f"Maintain a friendly, professional tone appropriate for user onboarding. "
        f"Preserve any placeholders, formatting, or special characters."
    )

    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": text},
        ],
        temperature=0.3,
        max_tokens=500,
    )

    translated = response.choices[0].message.content.strip()
    return translated


def translate_onboarding_copies(
    copies: list[dict],
    target_locale: str,
    source_locale: str = "en",
) -> list[dict]:
    results = []
    for copy_item in copies:
        key = copy_item.get("key", "")
        text = copy_item.get("text", "")
        translated = translate_onboarding_copy(
            text=text,
            target_locale=target_locale,
            source_locale=source_locale,
        )
        results.append(
            {
                "key": key,
                "text": text,
                "translated": translated,
                "locale": target_locale,
            }
        )
    return results


if __name__ == "__main__":
    sample_text = "Welcome! Let's get your account set up in just a few steps."
    result = translate_onboarding_copy(sample_text, target_locale="es")
    print(f"Original: {sample_text}")
    print(f"Spanish: {result}")
