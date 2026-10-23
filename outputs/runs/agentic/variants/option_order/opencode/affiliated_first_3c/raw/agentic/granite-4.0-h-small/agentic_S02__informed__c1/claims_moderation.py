from typing import List, Dict
from identity_models import NormalizedProfile


class ClaimModeration:
    """
    Moderate free‑text claims or notes attached to a user profile.
    The moderation step can enforce policy (e.g., profanity filtering,
    PII redaction) before the claims are persisted.
    """

    def __init__(self, moderation_handler):
        """
        Args:
            moderation_handler: a callable that receives (field_name: str, value: str)
                and returns a tuple (approved: bool, cleaned_value: str).
                The handler may be backed by a third‑party service like
                watsonx guardrails, Perspective API, etc.
        """
        self.moderation_handler = moderation_handler

    def moderate_profile(self, profile: NormalizedProfile) -> NormalizedProfile:
        """
        Iterate over all known text fields, run moderation, and replace
        with cleaned values when approval is granted.
        """
        # Example list of fields that may contain free text
        text_fields = ["name", "given_name", "family_name", "picture_url", "notes"]
        moderated_data: Dict[str, Any] = dict(profile)
        for field in text_fields:
            raw = getattr(profile, field, None)
            if raw:
                approved, cleaned = self.moderation_handler(field, raw)
                if approved:
                    moderated_data[field] = cleaned
                else:
                    # If moderation rejects, either drop the field or set to a placeholder
                    moderated_data[field] = "<redacted>"
        # Rebuild a NormalizedProfile instance
        return NormalizedProfile(**moderated_data)


# ---------------------------------------------------
# Example moderation handler using Watsonx Guardrails (optional)
# ---------------------------------------------------
# def watsonx_guardrails_moderate(field: str, value: str):
#     # ... call the watsonx guardrails API ...
#     return approved, cleaned_value
# ---------------------------------------------------
