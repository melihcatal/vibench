import re


def check_unsafe_labels(
    labels: list[str], unsafe_patterns: list[str] = None
) -> list[str]:
    """Screen secret labels for unsafe text based on regex patterns.

    Args:
        labels (list[str]): List of label strings attached to a secret.
        unsafe_patterns (list[str]): Regex patterns that denote unsafe content.
            If omitted, uses a basic list of profanity and PII snippets.

    Returns:
        list[str]: Labels that matched any unsafe pattern.
    """
    if unsafe_patterns is None:
        unsafe_patterns = [
            r"password|passwd|pw|secret|key|token|credential",
            r"\b\d{3}[-.]?\d{2}[-.]?\d{4}\b",  # SSN/credit card like pattern
            r"\b\d{4}[ -]\d{4}[ -]\d{4}[ -]\d{4}\b",  # credit card pattern
            r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",  # email addresses
        ]
    unsafe_flags = []
    combined = "|".join(f"({p})" for p in unsafe_patterns)
    pattern = re.compile(combined, re.IGNORECASE)
    for lbl in labels:
        if pattern.search(lbl):
            unsafe_flags.append(lbl)
    return unsafe_flags


# Example guard (not run in module)
if __name__ == "__main__":
    test = check_unsafe_labels(["prod-env", "user:pass123", "debug:1"])
    print(test)
