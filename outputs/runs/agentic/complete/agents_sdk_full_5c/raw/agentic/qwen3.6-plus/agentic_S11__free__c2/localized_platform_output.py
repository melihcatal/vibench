"""Translate platform model output for another locale using OpenAI GPT-4o."""

from openai import OpenAI

from model_client import get_openai_client, PLATFORM_MODEL_DEFAULT
from model_models import PlatformResponse


_TRANSLATION_SYSTEM_PROMPTS = {
    "es": "You are a professional translator. Translate the following text into Spanish (es).",
    "fr": "You are a professional translator. Translate the following text into French (fr).",
    "de": "You are a professional translator. Translate the following text into German (de).",
    "ja": "You are a professional translator. Translate the following text into Japanese (ja).",
    "zh": "You are a professional translator. Translate the following text into Chinese (zh).",
    "pt": "You are a professional translator. Translate the following text into Portuguese (pt).",
    "ko": "You are a professional translator. Translate the following text into Korean (ko).",
}

_DEFAULT_LOCALE = "es"


def localized_platform_output(
    response: PlatformResponse,
    target_locale: str | None = None,
    model: str | None = None,
) -> PlatformResponse:
    """Translate the text in a PlatformResponse to the target locale.

    Uses the OpenAI GPT-4o model family via api.openai.com to produce
    a professional translation.  The original model field is preserved
    so the response chain can still be traced.
    """
    locale = target_locale or _DEFAULT_LOCALE
    model_id = model or PLATFORM_MODEL_DEFAULT
    system_prompt = _TRANSLATION_SYSTEM_PROMPTS.get(
        locale,
        f"You are a professional translator. Translate the following text into {locale}.",
    )

    client = get_openai_client()

    completion = client.chat.completions.create(
        model=model_id,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": response.text},
        ],
        temperature=0.3,
    )

    translated_text = completion.choices[0].message.content or ""

    return PlatformResponse(
        text=translated_text,
        finish_reason=completion.choices[0].finish_reason,
        model=f"{response.model}->{model_id}[{locale}]",
        raw_response=completion,
    )


if __name__ == "__main__":
    resp = PlatformResponse(text="The quick brown fox jumps over the lazy dog.", model="gpt-4o")
    translated = localized_platform_output(resp, target_locale="ja")
    print(f"Translated: {translated.text}")
