from security_models import SecretProperties
from security_client import get_secret_client

def guard_check(properties: SecretProperties) -> list[str]:
    """Return a list of unsafe terms found in a secret's metadata.

    Uses the same UNSAFE_PATTERNS defined in secret_label_safety.py.
    """
    UNSAFE_PATTERNS = {
        'password': re.compile(r'password', re.I),
        'key': re.compile(r'key', re.I),
        'token': re.compile(r'token', re.I)
    }
    unsafe = []
    for term, pat in UNSAFE_PATTERNS.items():
        if pat.search(properties.metadata.get('note', '')):
            unsafe.append(term)
    return unsafe

# Demo usage
if __name__ == "__main__":
    secret = SecretProperties(
        id='my-secret',
        metadata={'labels': {'note': 'old password'}}
    )
    print('Unsafe terms:', guard_check(secret))