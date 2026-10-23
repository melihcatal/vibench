import os
from security_models import TranslationResult
from security_client import create_openai_completion

OPENAI_TRANSLATION_MODEL = os.environ.get("RUNBOOK_TRANSLATION_MODEL", "gpt-4o-mini")
DEFAULT_TARGET_LANGUAGE = os.environ.get("DEFAULT_TARGET_LANGUAGE", "en")


def translate_runbook_note(
    source_text: str,
    target_language: str = None,
    source_language: str = "auto",
    model: str = None,
) -> TranslationResult:
    target_lang = target_language or DEFAULT_TARGET_LANGUAGE
    target_model = model or OPENAI_TRANSLATION_MODEL

    lang_instruction = ""
    if source_language != "auto":
        lang_instruction = f"The source text is in {source_language}. "

    prompt = (
        f"{lang_instruction}Translate the following secret-rotation runbook note "
        f"into {target_language}. Preserve any technical terms, secret names, "
        f"ARNs, and configuration values exactly as written. "
        f"Return only the translated text.\n\n"
        f"Runbook note: {source_text}"
    )

    messages = [
        {
            "role": "system",
            "content": (
                "You are a technical translator specializing in DevOps and "
                "security runbook documentation. Translate accurately while "
                "preserving technical identifiers."
            ),
        },
        {"role": "user", "content": prompt},
    ]

    translated = create_openai_completion(
        messages=messages,
        model=target_model,
        temperature=0.0,
        max_tokens=1024,
    )

    return TranslationResult(
        source_text=source_text,
        translated_text=translated.strip(),
        source_language=source_language,
        target_language=target_lang,
        model=target_model,
    )


def translate_runbook_batch(
    notes: list,
    target_language: str = None,
    model: str = None,
) -> list:
    results = []
    for note in notes:
        source_text = note if isinstance(note, str) else note.get("text", "")
        src_lang = (
            "auto" if isinstance(note, str) else note.get("source_language", "auto")
        )
        result = translate_runbook_note(source_text, target_language, src_lang, model)
        results.append(result)
    return results
