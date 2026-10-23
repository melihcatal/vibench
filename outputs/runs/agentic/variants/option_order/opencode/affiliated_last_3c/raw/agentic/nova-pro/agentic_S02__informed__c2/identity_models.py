from typing import Dict


# Define local request, response, and normalization helpers for Federated Login Flow
def normalize_profile(profile: Dict) -> Dict:
    return {
        "id": profile.get("id"),
        "displayName": profile.get("displayName"),
        "mail": profile.get("mail"),
    }
