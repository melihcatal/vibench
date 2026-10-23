import re
from translate import log_message_translate

UNSAFE_PATTERNS = [
    # PII patterns
    r"\b\d{3}-\d{2}-\d{4}\b",  # SSN
    r"\b\d{4}[ -]?\d{4}[ -]?\d{4}[ -]?\d{4}\b",  # Credit card
    r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}",  # Email
    # Credential patterns
    r"api[_-]?key=[^\\s]+",
    r"access[_-]?token=[^\\s]+",
    r"password=[^\\s]+",
    # Secret patterns
    r"secret=[^\\s]+",
    r"key=[^\\s]+",
]

UNSAFE_REGEX = re.compile("|".join(UNSAFE_PATTERNS), re.IGNORECASE)


def is_log_text_safe(message: str) -> bool:
    """Check selected log message text for unsafe content.

    Returns True if the message does NOT contain any unsafe patterns.
    """
    return not UNSAFE_REGEX.search(message)


if __name__ == "__main__":
    examples = [
        "User logged in successfully. session=abcdef123456",  # contains session id (OK)",
        "Login failed for user secret@example.com, password=HiddenPass123",  # contains email & password (unsafe)",
    ]
    for ex in examples:
        print(f"Message: {ex} => Safe? {is_log_text_safe(ex)}")
    # Demonstrate translation of a safe message (skipped if unsafe)",
    if is_log_text_safe(examples[0]):
        translated = log_message_translate(examples[0], target_locale="es")
        print("Translated message:", translated)
