# refresh_session.py
# Refreshes an expired session or access token (same‑scenario implementation)

from typing import Dict, Any
import os

# ---------------------------------------------------------------------------
# Import local helper utilities
# ---------------------------------------------------------------------------
from email_password_login import refresh  # re‑use the shared refresh implementation

# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def refresh_session(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Public helper that callers can use when a session is stale.
    Expected payload: {"refresh_token": "..."}
    Returns a dict matching the shape defined in identity_models.LoginResponse.
    """
    # Delegate to the provider‑specific refresh routine
    return refresh(payload)


# ---------------------------------------------------------------------------
# Export for later‑step scripts (required by scoring)
# ---------------------------------------------------------------------------
__all__ = ["refresh_session"]
