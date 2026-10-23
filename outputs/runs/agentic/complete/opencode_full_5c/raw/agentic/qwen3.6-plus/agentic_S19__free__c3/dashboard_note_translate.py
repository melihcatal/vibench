from openai import OpenAI
from observability_models import TranslationResult


def translate_dashboard_note(
    note_text: str,
    target_locale: str,
    source_locale: str = "en",
    model: str = "gpt-4o-mini",
) -> TranslationResult:
    openai_client = OpenAI()

    system_prompt = (
        f"You are a professional translator specializing in technical and observability documentation. "
        f"Translate the provided dashboard note or metric annotation from {source_locale} to {target_locale}. "
        f"Preserve technical terms, metric names, and formatting. Only return the translated text."
    )

    completion = openai_client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": f"Translate this dashboard note to {target_locale}:\n\n{note_text}",
            },
        ],
        max_tokens=500,
        temperature=0.3,
    )

    translated_text = completion.choices[0].message.content.strip()

    return TranslationResult(
        original_text=note_text,
        translated_text=translated_text,
        source_locale=source_locale,
        target_locale=target_locale,
        model_used=model,
    )
