import os
import requests
from typing import Dict, List, Any


def validate_document_fields(fields: Dict[str, Any]) -> Dict[str, Any]:
    errors = []
    avg_conf = None
    if "confidence" in fields and fields["confidence"]:
        conf_values = [
            v for v in fields["confidence"].values() if isinstance(v, (int, float))
        ]
        if conf_values:
            avg_conf = sum(conf_values) / len(conf_values)
            if avg_conf < 0.8:
                errors.append(f"Average confidence {avg_conf:.2f} < 0.8")
    required = ["vendor_or_merchant", "date", "total"]
    missing = [
        k for k in required if k not in fields or fields[k] is None or fields[k] == ""
    ]
    if missing:
        errors.append(f"Missing: {missing}")
    vendor_text = fields.get("vendor_or_merchant", "")
    if vendor_text:
        toxicity = get_toxicity_score(vendor_text)
        if toxicity > 0.5:
            errors.append(f"Toxicity score {toxicity:.2f}")
    valid = len(errors) == 0
    return {"valid": valid, "errors": errors, "avg_confidence": avg_conf}


def get_toxicity_score(text: str) -> float:
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"
    payload = {
        "comment": {"text": text[:2000]},
        "requestedAttributes": {"TOXICITY": {}},
    }
    resp = requests.post(url, json=payload, timeout=10)
    if resp.status_code == 200:
        return resp.json()["attributeScores"]["TOXICITY"]["summaryScore"]["value"]
    return 0.0
