# [LATER-STEP] payload_safety.py - Check decrypted text payloads for unsafe content

import json
from typing import List, Tuple

# Example safety modules (one concrete provider is shown)
from alibabacloud_green import AlibabaCloudGreenClient  # <ALI_PROVIDER>

# Whitelisted safe patterns (regexes) – can be expanded
SAFE_PATTERNS = [
    r"^\s*[A-Za-z0-9_\\-. ]+\s*$",  # simple alphanumeric with common punctuation
    r"^\s*\\s*$",  # empty line
]

# Unsafe keywords – simplistic example
UNSAFE_KEYWORDS = [
    "password",
    "secret",
    "credential",
]


def scan_payload(text: str) -> Tuple[bool, List[str]]:
    """Scans the decrypted payload for safety violations.

    Returns:
        (is_safe, violations) where is_safe is True if the text passes all checks.
    """
    violations: List[str] = []
    # 1. Run through unsafe keywords
    for kw in UNSAFE_KEYWORDS:
        if kw.lower() in text.lower():
            violations.append(f"Unsafe keyword detected: '{kw}'")
    # 2. Run Alibaba Cloud Content Moderation (API call)
    client = AlibabaCloudGreenClient(
        access_key_id=os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID"),
        access_key_secret=os.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET"),
        region_id="cn-hangzhou",
    )
    try:
        response = client.text_moderation(
            text
        )  # pseudo‑method, replace with actual SDK call
        if response["code"] == "200" and response.get("suggestions").lower() != "pass":
            violations.append("Provider reported unsafe content")
    except Exception as exc:
        # Capture provider errors but do not fail the overall scan
        violations.append(f"Provider check failed: {exc}")
    # 3. Simple regex safety checks
    for pattern in SAFE_PATTERNS:
        if not any(re.fullmatch(pattern, text) for pattern in SAFE_PATTERNS):
            violations.append("Payload does not match allowed format")
            break  # only need one failure
    is_safe = len(violations) == 0
    return is_safe, violations


if __name__ == "__main__":
    test_text = "This is a safe message."
    safe, issues = scan_payload(test_text)
    print(json.dumps({"input": test_text, "safe": safe, "issues": issues}, indent=2))
