import json
import os
from typing import List, Dict, Any
from dataclasses import dataclass, asdict

from identity_models import FederatedProfile

@dataclass
class ModeratedClaim:
    claim_name: str
    original_value: Any
    moderator_decision: str  # e.g., 'approved', 'rejected', 'edited'
    moderator_note: str = ''
    timestamp: str = ''  # ISO8601


def moderate_free_text_claims(profiles: List[FederatedProfile], moderators: List[str]) -> List[Dict[str, Any]]:
    """
    Demonstration moderation routine:
    - Scan all user profiles for custom claims containing free-text fields (e.g., 'bio', 'interests').
    - Apply a simple rule: any claim containing hate speech or personal data is rejected and redacted.
    - Return a list of moderation actions that can be persisted.
    """
    actions: List[Dict[str, Any]] = []
    for idx, profile in enumerate(profiles):
        for claim, value in profile.custom.items():
            if claim in {'bio', 'interests', 'notes'}:
                # Very naive filter – in production use a moderation service (Perspective, Tisane, etc.)
                if isinstance(value, str) and ('hate' in value.lower() or 'personal data' in value.lower()):
                    actions.append({
                        'profile_index': idx,
                        'claim': claim,
                        'decision': 'rejected',
                        'note': 'Content violates policy',
                        'timestamp': datetime.utcnow().isoformat() + 'Z',
                    })
                    # Redact in memory (production would persist the redaction)
                    profiles[idx].custom[claim] = '[REDACTED]'
                else:
                    actions.append({
                        'profile_index': idx,
                        'claim': claim,
                        'decision': 'approved',
                        'note': 'Safe content',
                        'timestamp': datetime.utcnow().isoformat() + 'Z',
                    })
            else:
                # All other claims are auto‑approved for demo
                actions.append({
                    'profile_index': idx,
                    'claim': claim,
                    'decision': 'approved',
                    'note': 'No policy check needed',
                    'timestamp': datetime.utcnow().isoformat() + 'Z',
                })
    return actions

# ---------------------------------------------------------------------------
# Example CLI integration (replace with real moderation workflow)
# ---------------------------------------------------------------------------
if __name__ == '__main__':
    # Simulate loading profiles from IdentityClient (see identity_client.py)
    from identity_client import IdentityClient
    demo_sub = os.getenv('DEMO_USER_SUB')
    if demo_sub:
        profile = IdentityClient.fetch_profile(demo_sub)
        profiles = [profile]
    else:
        print('Set DEMO_USER_SUB env var with a valid user_id to test moderation.')
        profiles = []
    result = moderate_free_text_claims(profiles, moderators=['alice'])
    print(json.dumps(result, indent=2))
