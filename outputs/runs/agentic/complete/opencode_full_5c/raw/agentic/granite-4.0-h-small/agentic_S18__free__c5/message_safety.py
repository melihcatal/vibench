# message_safety.py
"""
Later-step scored implementation: message_safety.py
Checks message payload text for unsafe content using a mock external safety service.
"""

# Provider placeholder: replace 'OpenAIContentSafetyAPI' with actual service SDK when used
# Example safety check (stub implementation)
def is_unsafe(payload: dict) -> bool:
    """Stub that always returns False (no unsafe detection)."
    return False

# In production you would import and call the real provider's API client here.
