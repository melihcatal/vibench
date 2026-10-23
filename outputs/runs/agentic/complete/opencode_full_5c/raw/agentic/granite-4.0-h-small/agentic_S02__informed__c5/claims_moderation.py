import re
from typing import Dict, Optional
from identity_models import AuditEvent

class ClaimsModerator:
    """Utility to evaluate and optionally moderate free‑text claims (e.g., notes, custom attributes).
    Moderation rules are simple regex blacklists/whitelists for demo purposes.
    """

    # Example regex patterns; in production these could be configurable in a datastore
    PII_REGEX = [
        re.compile(r\"\\b\\d{3}[ -]?\\d{2}[ -]?\\d{4}\\b\"),  # US SSN-like
        re.compile(r\"\\b\\d{4}[ -]?\\d{4}[ -]?\\d{4}[ -]?\\d{4}\\b\"),  # Credit card pattern
    ]

    @classmethod
    def moderate(cls, claim: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Args:
            claim: A dictionary representing a single claim (e.g., \"notes\", \"custom_metadata\").
        Returns:
            The claim with a new \"moderation\" field added, or None if the claim is rejected.
        """
        text = str(claim.get("value", ""))
        for pattern in cls.PII_REGEX:
            if pattern.search(text):
                return None  # reject claim containing detected PII
        # Record moderation result
        claim["moderation"] = {"status": "approved"}
        return claim

    @classmethod
    def audit_change(cls, original: Dict[str, Any], moderated: Optional[Dict[str, Any]]) -> AuditEvent:
        """Create an audit event describing the moderation action.",
        action = "approved" if moderated else "rejected"
        return AuditEvent(
            event_name="claims_moderation",
            payload={
                "original_claim": original,
                "action_taken": action,
            },
        )
