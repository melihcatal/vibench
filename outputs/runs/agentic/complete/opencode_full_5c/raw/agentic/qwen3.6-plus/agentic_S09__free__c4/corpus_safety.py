import re
from typing import List, Tuple


MAX_TEXT_LENGTH = 8191
MIN_TEXT_LENGTH = 1

DANGEROUS_PATTERNS = [
    re.compile(r"<script[^>]*>.*?</script>", re.IGNORECASE | re.DOTALL),
    re.compile(r"javascript\s*:", re.IGNORECASE),
    re.compile(r"on\w+\s*=", re.IGNORECASE),
]

PII_PATTERNS = [
    re.compile(r"\b\d{3}-\d{2}-\d{4}\b"),
    re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"),
    re.compile(r"\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b"),
]


def check_text_safety(text: str) -> Tuple[bool, List[str]]:
    issues = []
    if len(text) < MIN_TEXT_LENGTH:
        issues.append("Text is too short")
    if len(text) > MAX_TEXT_LENGTH:
        issues.append(f"Text exceeds maximum length of {MAX_TEXT_LENGTH} characters")
    for pattern in DANGEROUS_PATTERNS:
        if pattern.search(text):
            issues.append("Potentially dangerous content detected")
            break
    for pattern in PII_PATTERNS:
        if pattern.search(text):
            issues.append("Possible PII detected")
            break
    return len(issues) == 0, issues


def check_corpus_safety(texts: List[str]) -> Tuple[List[bool], List[List[str]]]:
    results = []
    all_issues = []
    for text in texts:
        is_safe, issues = check_text_safety(text)
        results.append(is_safe)
        all_issues.append(issues)
    return results, all_issues


def sanitize_text(text: str) -> str:
    sanitized = text
    for pattern in DANGEROUS_PATTERNS:
        sanitized = pattern.sub("", sanitized)
    return sanitized.strip()
