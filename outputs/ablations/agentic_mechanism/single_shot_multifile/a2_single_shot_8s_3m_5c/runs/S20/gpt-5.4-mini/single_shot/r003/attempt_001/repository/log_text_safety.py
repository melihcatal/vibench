from google.cloud import aiplatform
from observability_models import SafetyCheckResult


def log_text_safety(text: str) -> SafetyCheckResult:
    unsafe_terms = ["password", "secret", "token", "ssn", "credit card"]
    reasons = [term for term in unsafe_terms if term in text.lower()]
    return SafetyCheckResult(is_safe=len(reasons) == 0, reasons=reasons)
