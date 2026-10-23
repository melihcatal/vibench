from dataclasses import dataclass
from typing import Dict, Any

# service: Microsoft Entra OIDC
# local normalization helpers


@dataclass
class FederatedProfile:
    user_id: str
    display_name: str
    email: str
    first_name: str
    last_name: str
    raw: Dict[str, Any] = None


def load_raw_profile(raw_json: str) -> Dict[str, Any]:
    return json.loads(raw_json)


# Example usage:
# raw = load_raw_profile('"{\"sub\":\"123\",\"name\":\"Alice\"}')
# profile = FederatedProfile(**raw)
# print(profile.email)
