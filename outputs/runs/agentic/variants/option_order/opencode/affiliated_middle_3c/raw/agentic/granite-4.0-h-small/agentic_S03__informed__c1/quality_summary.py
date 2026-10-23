def summarize_quality_issues(translated_texts: List[str]) -> str:
    """Create a brief summary of potential translation quality issues.

    This stub identifies simple problems: empty strings, repeated punctuation,
    or suspicious substrings (e.g., placeholders).
    """
    issues = []
    for idx, text in enumerate(translated_texts, start=1):
        if not text.strip():
            issues.append(f"Entry {idx}: empty or whitespace-only result.")
        # Placeholder like {0} or %s
        if re.search(r"{\d+}", text) or re.search(r"%[a-z]", text):
            issues.append(f"Entry {idx}: contains placeholder patterns.")
    if not issues:
        return "No obvious quality issues detected."
    return "\n".join(issues)
