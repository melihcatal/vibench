import re
from typing import List, Tuple
from embeddings_client import get_openai_client, get_embedding_model


MAX_TEXT_LENGTH = 8192
FORBIDDEN_PATTERNS = [
    re.compile(r"<script[^>]*>.*?</script>", re.IGNORECASE | re.DOTALL),
    re.compile(r"javascript\s*:", re.IGNORECASE),
    re.compile(r"data\s*:\s*text/html", re.IGNORECASE),
]


def _check_length(text: str) -> Tuple[bool, str]:
    if len(text) == 0:
        return False, "Text is empty"
    if len(text) > MAX_TEXT_LENGTH:
        return (
            False,
            f"Text exceeds maximum length of {MAX_TEXT_LENGTH} characters ({len(text)} chars)",
        )
    return True, ""


def _check_encoding(text: str) -> Tuple[bool, str]:
    try:
        text.encode("utf-8")
        return True, ""
    except UnicodeEncodeError:
        return False, "Text contains invalid UTF-8 characters"


def _check_injection_patterns(text: str) -> Tuple[bool, str]:
    for pattern in FORBIDDEN_PATTERNS:
        if pattern.search(text):
            return False, "Text contains potentially dangerous injection patterns"
    return True, ""


def _check_openai_moderation(text: str) -> Tuple[bool, str]:
    client = get_openai_client()
    try:
        moderation_response = client.moderations.create(input=text)
        result = moderation_response.results[0]
        if result.flagged:
            flagged_categories = [
                cat
                for cat, flagged in result.categories.model_dump().items()
                if flagged
            ]
            return (
                False,
                f"Text flagged by OpenAI moderation API for: {', '.join(flagged_categories)}",
            )
        return True, ""
    except Exception as e:
        return False, f"OpenAI moderation check failed: {str(e)}"


def check_corpus_text(text: str, run_moderation: bool = True) -> dict:
    checks = {
        "text_length": _check_length(text),
        "encoding": _check_encoding(text),
        "injection_patterns": _check_injection_patterns(text),
    }

    if run_moderation:
        checks["moderation"] = _check_openai_moderation(text)

    all_passed = all(passed for passed, _ in checks.values())

    issues = [msg for passed, msg in checks.values() if not passed]

    return {
        "safe": all_passed,
        "issues": issues,
        "checks": {
            name: {"passed": passed, "message": msg}
            for name, (passed, msg) in checks.items()
        },
    }


def check_corpus_batch(texts: List[str], run_moderation: bool = True) -> List[dict]:
    results = []
    for i, text in enumerate(texts):
        result = check_corpus_text(text, run_moderation=run_moderation)
        result["index"] = i
        results.append(result)
    return results


if __name__ == "__main__":
    import json

    test_texts = [
        "This is a safe text about programming.",
        "",
        "<script>alert('xss')</script>",
        "A normal sentence with no issues whatsoever.",
    ]
    results = check_corpus_batch(test_texts, run_moderation=True)
    for r in results:
        print(f"Index {r['index']}: safe={r['safe']}, issues={r['issues']}")
