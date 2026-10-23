import os
# Conceptual integration with Azure Content Moderator

def check_message_safety(message_text: str):
    # In a real scenario, this would call Azure Content Moderator API.
    # For demonstration, we just simulate a check.
    is_safe = "unsafe" not in message_text.lower()
    safety_report = {
        "is_safe": is_safe,
        "flagged_terms": ["unsafe"] if not is_safe else [],
        "_provider_signal": "Azure Content Moderator (conceptual)"
    }
    return safety_report
