from typing import Union
import re


def check_payload_safety(payload: Union[str, bytes], check_type: str = "all") -> dict:
    if isinstance(payload, bytes):
        payload = payload.decode("utf-8", errors="ignore")

    results = {
        "is_safe": True,
        "checks": {},
        "unsafe_patterns": [],
    }

    patterns = {
        "sql_injection": r"(\b(SELECT|INSERT|UPDATE|DELETE|DROP|ALTER|CREATE|TRUNCATE|EXEC(UTE)?|DECLARE)\b|(\b(OR|AND)\b\s+[0-9]+\s*=[0-9]+)|(--|#|/\*|\*/|;))",
        "xss": r"(<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>)|(javascript:\s*[^"]+)|(on\w+\s*=)",
        "ssrf": r"(http:\/\/|https:\/\/|ftp:\/\/|file:\/\/|localhost|127\.0\.0\.1|::1|0\.0\.0\.0|169\.254\.|192\.168\.|10\.|172\.(1[6-9]|2[0-9]|3[0-1]))",
        "command_injection": r"(\b(sh|bash|cmd|powershell|python|perl|ruby|php)\b|(\||&|;|`|\$\()|(\b(rm|mv|cp|cat|echo|ls|wget|curl|chmod)\b))",
        "sensitive_data": r"(\b(password|secret|api_key|token|credit_card|ssn)\b\s*[:=]\s*[\"']?[^\s\"',;]+)|(\b(?:4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14}|3[47][0-9]{13}|6(?:011|5[0-9]{2})[0-9]{12})\b)",
    }

    checks_to_run = []
    if check_type == "all":
        checks_to_run = patterns.keys()
    else:
        checks_to_run = [check_type] if check_type in patterns else []

    for check in checks_to_run:
        matches = re.findall(patterns[check], payload, re.IGNORECASE)
        if matches:
            results["is_safe"] = False
            results["checks"][check] = False
            results["unsafe_patterns"].extend([match[0] for match in matches if match[0]])
        else:
            results["checks"][check] = True

    return results