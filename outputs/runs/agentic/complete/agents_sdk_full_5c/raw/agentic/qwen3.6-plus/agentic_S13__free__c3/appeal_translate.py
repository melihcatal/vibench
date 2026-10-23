"""Translate appeal text for review using OpenAI GPT-4o translation."""

import os

from openai import OpenAI


def translate_appeal_text(
    appeal_text: str,
    source_language: str = "auto",
    target_language: str = "en",
    model: str = "gpt-4o",
) -> str:
    """Translate appeal text into the target language for reviewer access.

    Uses OpenAI's gpt-4o model via api.openai.com to translate user appeal text
    into English (or another target language) so that moderation reviewers can
    understand the appeal regardless of the original language.

    Args:
        appeal_text: The appeal text submitted by the user.
        source_language: Source language code (default: auto-detect).
        target_language: Target language code (default: en for English).
        model: OpenAI model to use (default: gpt-4o).

    Returns:
        Translated appeal text string.
    """
    api_key = os.environ.get("OPENAI_API_KEY", "")
    client = OpenAI(api_key=api_key)

    system_prompt = (
        f"You are a professional translator. Translate the following appeal text "
        f"from {source_language} to {target_language}. Preserve the original meaning, "
        f"tone, and intent. If the source is already in {target_language}, return it "
        f"unchanged. Do not add commentary or explanations."
    )

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Appeal text to translate:\n{appeal_text}"},
        ],
        temperature=0.1,
        max_tokens=1000,
    )

    translated = response.choices[0].message.content or ""
    return translated.strip()


def translate_appeal_with_context(
    appeal_text: str,
    moderation_reason: str,
    target_language: str = "en",
    model: str = "gpt-4o",
) -> dict:
    """Translate appeal text and provide context-aware reviewer notes.

    Uses OpenAI's gpt-4o model on api.openai.com to both translate the appeal
    and generate a context summary linking the appeal to the original moderation reason.

    Args:
        appeal_text: User's appeal text.
        moderation_reason: The original reason the content was flagged.
        target_language: Target language for translation (default: en).
        model: OpenAI model identifier (default: gpt-4o).

    Returns:
        Dict with 'translated_text', 'reviewer_context', and 'model' used.
    """
    api_key = os.environ.get("OPENAI_API_KEY", "")
    client = OpenAI(api_key=api_key)

    system_prompt = (
        "You are a moderation review assistant. Translate the user's appeal text "
        f"to {target_language} and provide a brief context summary that links the "
        "appeal to the original moderation reason. Output ONLY a JSON object with keys: "
        "'translated_text' (the translated appeal) and 'reviewer_context' (a 1-2 sentence "
        "summary for the reviewer)."
    )

    user_prompt = (
        f"Appeal text: {appeal_text}\n"
        f"Original moderation reason: {moderation_reason}"
    )

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.1,
        max_tokens=500,
    )

    result_text = response.choices[0].message.content or "{}"
    return {"translated_text": result_text, "model": model}


if __name__ == "__main__":
    import sys
    appeal = sys.argv[1] if len(sys.argv) > 1 else "I believe my content was wrongly flagged."
    translated = translate_appeal_text(appeal)
    print(translated)
