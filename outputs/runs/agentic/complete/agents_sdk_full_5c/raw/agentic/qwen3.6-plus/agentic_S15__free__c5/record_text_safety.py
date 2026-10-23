"""
Check user-generated document fields for unsafe content using OpenAI Moderation API.
"""

import os

from openai import OpenAI

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
OPENAI_MODERATION_MODEL = "text-moderation-stable"


def check_text_safety(text: str) -> dict:
    """
    Run a safety check on a single text string using OpenAI's moderation model.

    Parameters
    ----------
    text : str
        The user-generated text to evaluate.

    Returns
    -------
    dict
        A dict with keys:
        - ``flagged`` (bool)
        - ``categories`` (dict[str, bool])
        - ``category_scores`` (dict[str, float])
    """
    client = OpenAI(api_key=OPENAI_API_KEY)

    result = client.moderations.create(
        model=OPENAI_MODERATION_MODEL,
        input=text,
    )

    mod_result = result.results[0]
    return {
        "flagged": mod_result.flagged,
        "categories": dict(mod_result.categories),
        "category_scores": dict(mod_result.category_scores),
    }


def check_document_safety(document: dict) -> dict:
    """
    Check all string-valued fields in a document for unsafe content.

    Parameters
    ----------
    document : dict
        A document record with arbitrary fields.

    Returns
    -------
    dict
        Mapping of field name to its safety result dict (see ``check_text_safety``).
        Fields with non-string values are skipped.
    """
    results = {}
    for key, value in document.items():
        if isinstance(value, str) and value.strip():
            results[key] = check_text_safety(value)
    return results
