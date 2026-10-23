import re
from openai import OpenAI
from embeddings_client import get_openai_client


MAX_TEXT_LENGTH = 8192
MIN_TEXT_LENGTH = 1

DANGEROUS_PATTERNS = [
    re.compile(r"<script[^>]*>.*?</script>", re.IGNORECASE | re.DOTALL),
    re.compile(r"javascript\s*:", re.IGNORECASE),
    re.compile(r"on\w+\s*=", re.IGNORECASE),
    re.compile(r"eval\s*\(", re.IGNORECASE),
    re.compile(r"__import__\s*\(", re.IGNORECASE),
    re.compile(r"exec\s*\(", re.IGNORECASE),
]

PERSONAL_DATA_PATTERNS = [
    re.compile(r"\b\d{3}-\d{2}-\d{4}\b"),
    re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"),
    re.compile(r"\b\d{13,19}\b"),
]


def check_corpus_text(
    text, max_length=MAX_TEXT_LENGTH, min_length=MIN_TEXT_LENGTH, api_key=None
):
    issues = []
    if len(text) < min_length:
        issues.append(
            {
                "type": "too_short",
                "message": f"Text length {len(text)} is below minimum {min_length}",
            }
        )
    if len(text) > max_length:
        issues.append(
            {
                "type": "too_long",
                "message": f"Text length {len(text)} exceeds maximum {max_length}",
            }
        )
    for pattern in DANGEROUS_PATTERNS:
        if pattern.search(text):
            issues.append(
                {
                    "type": "dangerous_content",
                    "message": f"Potentially dangerous pattern detected: {pattern.pattern}",
                }
            )
    for pattern in PERSONAL_DATA_PATTERNS:
        if pattern.search(text):
            issues.append(
                {
                    "type": "personal_data",
                    "message": f"Potential personal data detected: {pattern.pattern}",
                }
            )
    safe = len(issues) == 0
    client = get_openai_client(api_key=api_key)
    moderation_response = client.moderations.create(input=text)
    moderation_result = moderation_response.results[0]
    if moderation_result.flagged:
        for category, flagged in moderation_result.categories.model_dump().items():
            if flagged:
                issues.append(
                    {
                        "type": "content_moderation",
                        "message": f"Flagged by OpenAI moderation API: {category}",
                    }
                )
        safe = False
    return {"safe": safe, "issues": issues, "text_length": len(text)}


def sanitize_text(text):
    sanitized = text
    for pattern in DANGEROUS_PATTERNS:
        sanitized = pattern.sub("", sanitized)
    return sanitized.strip()


def filter_safe_texts(texts, api_key=None):
    safe_texts = []
    for text in texts:
        result = check_corpus_text(text, api_key=api_key)
        if result["safe"]:
            safe_texts.append(text)
    return safe_texts


if __name__ == "__main__":
    import sys

    text = (
        sys.argv[1] if len(sys.argv) > 1 else "This is a safe test text for embedding."
    )
    result = check_corpus_text(text)
    print(f"Safe: {result['safe']}")
    print(f"Text length: {result['text_length']}")
    if result["issues"]:
        for issue in result["issues"]:
            print(f"  Issue: {issue['type']} - {issue['message']}")
    else:
        print("  No issues found")
