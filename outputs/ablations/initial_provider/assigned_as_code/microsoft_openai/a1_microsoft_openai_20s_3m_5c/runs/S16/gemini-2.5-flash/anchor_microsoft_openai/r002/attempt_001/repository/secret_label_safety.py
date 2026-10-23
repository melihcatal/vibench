from security_models import AuditNote
from typing import List, Dict

UNSAFE_KEYWORDS = ["password", "secret", "key", "token", "credential", "confidential", "private"]

def check_label_safety(audit_note: AuditNote) -> Dict[str, Any]:
    unsafe_findings = []

    # Check content of the audit note
    for keyword in UNSAFE_KEYWORDS:
        if keyword in audit_note.content.lower():
            unsafe_findings.append({"type": "content", "keyword": keyword, "match": keyword})

    # Check labels of the audit note
    if audit_note.labels:
        for label_key, label_value in audit_note.labels.items():
            for keyword in UNSAFE_KEYWORDS:
                if keyword in label_key.lower():
                    unsafe_findings.append({"type": "label_key", "keyword": keyword, "match": label_key})
                if keyword in label_value.lower():
                    unsafe_findings.append({"type": "label_value", "keyword": keyword, "match": label_value})

    return {
        "note_id": audit_note.note_id,
        "secret_id": audit_note.secret_id,
        "is_safe": not bool(unsafe_findings),
        "findings": unsafe_findings
    }
