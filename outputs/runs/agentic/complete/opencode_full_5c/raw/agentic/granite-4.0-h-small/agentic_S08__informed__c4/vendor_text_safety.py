import os
import re
from validate_document_fields import validate_document_fields

# Tisane API credentials (replace with real secrets in production)
TISANE_API_KEY = os.getenv("TISANE_API_KEY")


def moderate_vendor_notes(extracted: dict) -> dict:
    """
    Moderate vendor notes or memo fields for policy violations using Tisane.
    Passes the note text to Tisane and returns a moderation verdict.
    """
    note = extracted.get("vendor_notes", "")
    if not note:
        return {"moderation": "skip", "reason": "no notes"}
    # Placeholder for Tisane SDK call; here we simulate a simple check
    if re.search(r"(illegal|fraud|scam)", note, re.I):
        return {"moderation": "reject", "reason": "contains prohibited content"}
    return {"moderation": "allow", "reason": "no issues"}


# Example usage (uncomment to test)
# sample = {'vendor_notes':'This is a legitimate vendor.'}
# print(moderate_vendor_notes(sample))
