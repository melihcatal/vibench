from model_client import create_openai_client, OPENAI_API_BASE


LOCALE_SYSTEM_PROMPTS = {
    "es": "You are a professional translator. Translate the following text into Spanish. Preserve formatting and tone.",
    "fr": "You are a professional translator. Translate the following text into French. Preserve formatting and tone.",
    "de": "You are a professional translator. Translate the following text into German. Preserve formatting and tone.",
    "ja": "You are a professional translator. Translate the following text into Japanese. Preserve formatting and tone.",
    "zh": "You are a professional translator. Translate the following text into Chinese (Simplified). Preserve formatting and tone.",
    "pt": "You are a professional translator. Translate the following text into Portuguese. Preserve formatting and tone.",
    "ko": "You are a professional translator. Translate the following text into Korean. Preserve formatting and tone.",
    "ar": "You are a professional translator. Translate the following text into Arabic. Preserve formatting and tone.",
}


def localize_platform_output(
    text: str,
    target_locale: str,
    source_locale: str = "en",
    model: str = "gpt-4o",
) -> str:
    system_prompt = LOCALE_SYSTEM_PROMPTS.get(
        target_locale,
        f"You are a professional translator. Translate the following text into {target_locale}. Preserve formatting and tone.",
    )
    client = create_openai_client(base_url=OPENAI_API_BASE)
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": text},
    ]
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.3,
        max_tokens=4096,
    )
    return response.choices[0].message.content or ""
