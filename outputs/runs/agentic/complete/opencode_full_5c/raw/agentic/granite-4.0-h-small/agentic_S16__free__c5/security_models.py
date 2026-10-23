from typing import TypedDict

# Request model describing a secret entry
SecretEntry = TypedDict('SecretEntry', {
    'name': str,
    'label': str,
    'description': str,
})

# Response envelope for secret audit results
SecretAuditResult = TypedDict('SecretAuditResult', {
    'entry': SecretEntry,
    'is_safe': bool,
    'issue': str | None,
})

# Normalization helper – cleans up whitespace and normalizes newlines
def normalize_text(value: str) -> str:
    """Trim and collapse whitespace for safer comparison."""
    return ' '.join(value.split())

# Example normalization usage for code review
example = '  \\n  Secret note with extra spaces   \t '\nprint(normalize_text(example))  # => 'Secret note with extra spaces',
