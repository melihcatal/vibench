import json
from typing import Dict, Any

def check_decrypted_payload(payload: str, unsafe_keywords: list = None) -> Dict[str, Any]:
    """Scans a plaintext payload for disallowed or unsafe content.

    Args:
        payload (str): The UTF‑8 plaintext to inspect.
        unsafe_keywords (list): Optional list of terms considered unsafe.
                               If omitted, uses a built‑in default list.

    Returns:
        Dict[str, Any]: A report indicating whether the payload is safe and details.
    """
    if unsafe_keywords is None:
        unsafe_keywords = [
            "password",
            "passwd",
            "secret",
            "apikey",
            "token",
            "credential",
            "privatekey",
            "ssh",
            "creditcard",
            "ccnumber",
        ]
    report = {"safe": True, "reasons": []}
    lower_payload = payload.lower()
    for kw in unsafe_keywords:
        if kw.lower() in lower_payload:
            report["safe"] = False
            report["reasons"].append(f"Contains unsafe keyword: {kw}")
    return report

if __name__ == "__main__":
    # Example usage – replace with actual decrypted text
    sample = "User password: SuperSecret123 and API token: abcdef123456"
    print(json.dumps(check_decrypted_payload(sample), indent=2))
