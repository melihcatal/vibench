# quality_summary.py
from translation_models import normalize_response

def summarize_quality(translation: str) -> str:
    """Provide a short quality summary for a translated string.
    Currently flags potential issues like HTML artifacts or placeholder text.
    """
    summary = []
    if "<" in translation and ">" in translation:
        summary.append("Translation contains HTML tags - may need cleanup.")
    if "__PLACEHOLDER_" in translation:
        summary.append("Translation contains placeholder tokens - extraction step may have missed content.")
    if not translation:
        summary.append("Translation was empty.")
    return "Quality Summary:\n" + "\n".join(summary)
