from typing import List, Dict, Tuple
import re
from openai import OpenAI
from embeddings_client import build_embeddings_client, load_config_from_env


MAX_TEXT_LENGTH = 8191
MIN_TEXT_LENGTH = 1
INVALID_CHAR_PATTERN = re.compile(r"[\x00-\x08\x0B\x0C\x0E-\x1F\x7F-\x9F]")
URL_PATTERN = re.compile(r"https?://\S+")
EMAIL_PATTERN = re.compile(r"\S+@\S+\.\S+")


def check_text_length(text: str, max_length: int = MAX_TEXT_LENGTH) -> Tuple[bool, str]:
    if len(text) < MIN_TEXT_LENGTH:
        return False, f"Text is too short (minimum {MIN_TEXT_LENGTH} characters)"
    if len(text) > max_length:
        return False, f"Text exceeds maximum length of {max_length} characters"
    return True, "OK"


def check_text_encoding(text: str) -> Tuple[bool, str]:
    try:
        text.encode("utf-8")
        return True, "OK"
    except UnicodeEncodeError as e:
        return False, f"Encoding error: {str(e)}"


def check_invalid_characters(text: str) -> Tuple[bool, str]:
    matches = (
        INVALID_PATTERN.findall(text)
        if hasattr(globals().get("INVALID_PATTERN", None), "findall")
        else INVALID_CHAR_PATTERN.findall(text)
    )
    if matches:
        return False, f"Found {len(matches)} invalid control characters"
    return True, "OK"


def check_pii_content(text: str) -> Tuple[bool, List[str]]:
    findings = []
    emails = EMAIL_PATTERN.findall(text)
    if emails:
        findings.append(f"Email addresses found: {len(emails)}")
    urls = URL_PATTERN.findall(text)
    if urls:
        findings.append(f"URLs found: {len(urls)}")
    phone_pattern = re.compile(r"\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b")
    phones = phone_pattern.findall(text)
    if phones:
        findings.append(f"Phone numbers found: {len(phones)}")
    if findings:
        return False, findings
    return True, []


def check_corpus_safety(text: str) -> Dict:
    length_ok, length_msg = check_text_length(text)
    encoding_ok, encoding_msg = check_text_encoding(text)
    chars_ok, chars_msg = check_invalid_characters(text)
    pii_ok, pii_findings = check_pii_content(text)
    is_safe = length_ok and encoding_ok and chars_ok
    return {
        "is_safe": is_safe,
        "checks": {
            "length": {"passed": length_ok, "message": length_msg},
            "encoding": {"passed": encoding_ok, "message": encoding_msg},
            "invalid_characters": {"passed": chars_ok, "message": chars_msg},
            "pii_detection": {"passed": pii_ok, "findings": pii_findings},
        },
    }


def validate_corpus_batch(texts: List[str]) -> List[Dict]:
    results = []
    for i, text in enumerate(texts):
        safety = check_corpus_safety(text)
        results.append(
            {
                "index": i,
                "text_preview": text[:50] + ("..." if len(text) > 50 else ""),
                "is_safe": safety["is_safe"],
                "checks": safety["checks"],
            }
        )
    return results


def sanitize_text(text: str) -> str:
    sanitized = INVALID_CHAR_PATTERN.sub("", text)
    sanitized = re.sub(r"\s+", " ", sanitized).strip()
    return sanitized


def filter_safe_corpus(texts: List[str]) -> List[str]:
    safe_texts = []
    for text in texts:
        safety = check_corpus_safety(text)
        if safety["is_safe"]:
            safe_texts.append(sanitize_text(text))
    return safe_texts


def check_openai_moderation(text: str) -> Dict:
    config = load_config_from_env()
    client: OpenAI = build_embeddings_client(api_key=config["api_key"])
    response = client.moderations.create(
        model="omni-moderation-latest",
        input=text,
    )
    result = response.results[0]
    return {
        "flagged": result.flagged,
        "categories": {
            "hate": result.categories.hate,
            "hate_threatening": result.categories.hate_threatening,
            "self_harm": result.categories.self_harm,
            "sexual": result.categories.sexual,
            "sexual_minors": result.categories.sexual_minors,
            "violence": result.categories.violence,
            "violence_graphic": result.categories.violence_graphic,
        },
        "category_scores": {
            "hate": result.category_scores.hate,
            "hate_threatening": result.category_scores.hate_threatening,
            "self_harm": result.category_scores.self_harm,
            "sexual": result.category_scores.sexual,
            "sexual_minors": result.category_scores.sexual_minors,
            "violence": result.category_scores.violence,
            "violence_graphic": result.category_scores.violence_graphic,
        },
    }


def check_corpus_safety_with_moderation(text: str) -> Dict:
    local_safety = check_corpus_safety(text)
    moderation = check_openai_moderation(text)
    is_safe = local_safety["is_safe"] and not moderation["flagged"]
    return {
        "is_safe": is_safe,
        "local_checks": local_safety,
        "openai_moderation": moderation,
    }


if __name__ == "__main__":
    test_texts = [
        "This is a safe text for embedding",
        "Contact us at support@example.com or call 555-123-4567",
        "",
        "A" * 9000,
    ]
    results = validate_corpus_batch(test_texts)
    for r in results:
        status = "SAFE" if r["is_safe"] else "UNSAFE"
        print(f"[{status}] Index {r['index']}: {r['text_preview']}")
