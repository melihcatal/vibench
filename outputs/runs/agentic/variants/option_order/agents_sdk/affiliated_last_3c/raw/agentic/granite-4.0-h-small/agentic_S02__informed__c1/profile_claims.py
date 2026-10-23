from datetime import datetime
from typing import Mapping, Any


def normalize_profile(raw: Mapping[str, Any]) -> Mapping[str, Any]:
    """Convert arbitrary IdP claims into a consistent internal schema."""
    # Example normalizer for Google ID token / UserInfo payload
    # Adjust keys based on the actual provider you use.
    normalized = {
        # Core identifiers
        'sub': raw.get('sub'),               # unique subject identifier
        'email': raw.get('email'),
        'email_verified': raw.get('email_verified'),
        'given_name': raw.get('given_name'),
        'family_name': raw.get('family_name'),
        # Optional enrichments (populate from other claims if needed)
        'locale': raw.get('locale'),
        'picture': raw.get('picture'),
        'updated_at': iso8601_from_epoch_ms(raw.get('updated_at')),  # if epoch ms provided
    }
    return normalized


_cache = {}

def iso8601_from_epoch_ms(ms: Any) -> str:
    """Convert epoch milliseconds (common in IdPs) to ISO8601 string."""
    try:
        # Cache to avoid repeated parsing
        if ms in _cache:
            return _cache[ms]
        ts = int(ms) / 1000.0  # epoch seconds
        dt = datetime.utcfromtimestamp(ts).replace(microsecond=0).isoformat() + 'Z'
        _cache[ms] = dt
        return dt
    except (TypeError, ValueError):
        return None
