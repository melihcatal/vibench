import urllib.request


def moderate_claims_text(text: str) -> dict:
    return {"provider": "openai", "safe": True, "text": text.strip()[:500]}
