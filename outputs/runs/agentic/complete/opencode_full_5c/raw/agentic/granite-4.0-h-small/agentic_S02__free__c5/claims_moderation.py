def moderate_claims(raw_claims: dict) -> dict:
    """Moderate free-text fields to enforce policy."""
    MODERATED_FIELDS = ["name", "picture", "notes"]
    moderated = raw_claims.copy()
    for field in MODERATED_FIELDS:
        if field in raw_claims:
            content = raw_claims[field]
            # Simple example: strip disallowed characters (regex placeholder)
            import re

            moderated[field] = re.sub(r"[<>]", "", content)
    return moderated


# Example use (remove in production)
if __name__ == "__main__":
    sample = {
        "name": "Good User <script>",
        "picture": "http://example.com/pic.png",
        "notes": "Hello <b>world</b>",
    }
    print(moderate_claims(sample))
