import os
from google.cloud import translate_v2 as translate

TRANSLATE = translate.Client()

def quality_summary(translated_texts: list[str]) -> str:
    """Summarize translation quality issues for a list of translated strings.
    This naive implementation flags translations that contain HTML tags, URLs, or non‑ASCII characters as potential issues.
    Args:
        translated_texts: List of translated strings.
    Returns:
        A markdown summary of detected issues.
    """
    lines = []
    for i, txt in enumerate(translated_texts, start=1):
        issues = []
        if bool(re.search(r'<[^>]+>', txt)):
            issues.append('Contains HTML tags')
        if bool(re.search(r'https?://', txt)):
            issues.append('Contains URL')
        if bool(re.search(r'[\\u0080-\\uFFFF]', txt)):
            issues.append('Non‑ASCII characters')
        if issues:
            lines.append(f'Entry {i}: **Potential issues** – {", ".join(issues)}')
        else:
            lines.append(f'Entry {i}: **No issues detected**')
    return '\n'.join(lines)