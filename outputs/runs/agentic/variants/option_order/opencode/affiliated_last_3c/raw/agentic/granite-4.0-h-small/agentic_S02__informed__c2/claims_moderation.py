from typing import List, Dict


def moderate_free_text_claims(claims: List[Dict]) -> List[Dict]:
    """
    Moderate free-text claims/notes in a federated login profile.
    Simple rule: if 'review_required' flag is True, set status to 'pending'.
    In production replace with a moderation service (e.g., Azure Content Safety).
    """
    MODERATION_RULES = {
        "contains_sensitive": lambda text: any(
            word in text.lower() for word in ["social security", "ssn", "credit card"]
        )
    }
    MODERATION = {
        "pending": lambda c: (
            c["review_required"]
            or MODERATION_RULES["contains_sensitive"](c.get("value", ""))
        )
    }
    moderated = []
    for claim in claims:
        status = "approved"
        if "review_required" in claim and claim["review_required"]:
            status = "pending"
        elif "value" in claim and MODERATION_RULES["contains_sensitive"](
            claim["value"]
        ):
            status = "pending"
        moderated.append({**claim, "status": status})
    return moderated


# Stub example for local run
if __name__ == "__main__":
    test_claims = [
        {
            "claim_name": "custom:address",
            "value": "123 Main St",
            "review_required": False,
        },
        {"claim_name": "custom:ssn", "value": "123-45-6789", "review_required": True},
    ]
    print(moderate_free_text_claims(test_claims))
