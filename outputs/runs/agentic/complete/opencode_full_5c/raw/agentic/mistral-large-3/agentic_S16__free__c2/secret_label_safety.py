import re
from security_models import SecretSafetyCheck


def check_secret_labels(
    secret_id: str, labels: dict, notes: str = None
) -> SecretSafetyCheck:
    unsafe_reasons = []

    if labels:
        for key, value in labels.items():
            if re.search(r"password|secret|key|token|credential", key, re.IGNORECASE):
                unsafe_reasons.append(f"Unsafe label key: {key}")
            if re.search(r"password|secret|key|token|credential", value, re.IGNORECASE):
                unsafe_reasons.append(f"Unsafe label value: {value}")

    if notes:
        if re.search(
            r"password\s*=\s*[^\s]+|secret\s*=\s*[^\s]+|key\s*=\s*[^\s]+",
            notes,
            re.IGNORECASE,
        ):
            unsafe_reasons.append("Unsafe note containing credential-like patterns")

    return SecretSafetyCheck(
        secret_id=secret_id,
        is_safe=len(unsafe_reasons) == 0,
        unsafe_reasons=unsafe_reasons,
        labels=labels,
        notes=notes,
    )
