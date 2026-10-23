import os
import json
import re

def moderate_free_text_claims(claims):
    """
    Apply simple policy checks to free-text claims (e.g., notes, custom strings).
    Policy examples:
      - No hate, harassment, or extremist language (basic keyword filter)
      - No PII such as raw email addresses or phone numbers
      - Truncate overly long text (>256 chars)
    Returns a sanitized copy of the claims dict.
    """
    MODERATION_REGEXES = [
        # Simple keyword filter (case-insensitive)
        re.compile(r'\b(?:hate|violence|terror|offensive)\b', re.IGNORECASE),
        # Detect email-like strings
        re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b'),
        # Detect phone number patterns
        re.compile(r'\b\+?\d{10,15}\b')
    ]
    sanitized = claims.copy()
    for key, value in sanitized.items():
        if isinstance(value, str):
            # Truncate overly long strings
            if len(value) > 256:
                sanitized[key] = value[:253] + '...'
            # Scan for policy violations
            for regex in MODERATION_REGEXES:
                if regex.search(value):
                    # Replace offending substring with [REDACTED]
                    def repl(m):
                        return '[REDACTED]'
                    value = regex.sub(repl, value)
                    sanitized[key] = value
    return sanitized

if __name__ == '__main__':
    # Example usage with static claims dictionary
    sample_claims = {
        'name': 'John Doe',
        'notes': 'This user is a terrorist sympathizer and should be blocked.',
        'custom': 'email@example.com, call +1234567890'
    }
    print('Original claims:', json.dumps(sample_claims, indent=2))
    moderated = moderate_free_text_claims(sample_claims)
    print('Moderated claims:', json.dumps(moderated, indent=2))