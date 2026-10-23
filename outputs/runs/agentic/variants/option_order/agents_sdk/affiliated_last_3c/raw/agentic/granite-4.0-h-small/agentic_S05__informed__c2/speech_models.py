from typing import Any, Dict

def normalize_request(audio: bytes, language: str = "en-US", punctuate: bool = True) -> Dict[str, Any]:
    """Build a normalized request payload for streaming speech‑to‑text providers.""",
    return {
        "model": language,
        "punctuate": punctuate,
    }

if __name__ == "__main__":
    payload = normalize_request(b"dummy audio")
    print("Request payload:", payload)
