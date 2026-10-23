import os
from google.genai import ContentReference, HarmType, HarmSeverity

# Use Gemini model for summarising translation quality issues
model = "gemini-1.5-flash"


def summarize_quality(translated_texts):
    """Summarize quality issues found in a list of translated texts.

    Args:
        translated_texts (list[str]): outputs from a translation service.

    Returns:
        dict: summary with overall rating and list of flagged issues.
    """
    # Build a combined prompt for the LLM
    prompt = (
        "You are a translation quality reviewer. For each string below, identify any of the following issues:\\n"
        "- mistranslation\\n- untranslated placeholder\\n- grammatical error\\n- verbose or awkward phrasing\\n- unsafe content (e.g., hate, self‑harm, sexual content)\\n"
        'Provide a concise bullet list: one bullet per issue type, prefixed with the string index (starting at 1). If no issues, state "No issues found".\\n'
        "Strings to review:\\n"
        + "\\n".join(f"{i + 1}: {t}" for i, t in enumerate(translated_texts))
    )

    # Configure Gemini request with guardrails
    from google.genai import HarmBlockThreshold

    response = model.generate_content(
        prompt,
        generation_config={
            "temperature": 0.0,
            "max_output_tokens": 500,
        },
        safety_settings={
            HarmType.HARMS_CATEGORY_TOXICITY: HarmSeverity.BLOCK_MEDIUM_AND_ABOVE,
            HarmType.HARMS_CATEGORY_HATE: HarmSeverity.BLOCK_ALL,
        },
    )

    summary = response.text.strip()
    return {"summary": summary, "provider": "Gemini"}
