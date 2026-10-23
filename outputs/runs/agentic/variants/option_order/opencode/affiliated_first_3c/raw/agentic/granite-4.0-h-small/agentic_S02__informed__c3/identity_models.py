from typing import NamedTuple, Any


class FederatedProfile(NamedTuple):
    sub: str
    name: str
    email: str
    email_verified: bool
    picture: str
    # Add additional normalized fields here
    extra: dict[str, Any] = frozendict()  # Optional extra claims


class ClaimNormalizationError(Exception):
    """Raised when claim extraction/normalization fails."""


class PersistedAuditRecord(NamedTuple):
    user_sub: str
    event_type: str
    details: dict[str, Any]
    timestamp: str
