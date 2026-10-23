from typing import Dict


class IdentityRequest:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


class IdentityResponse:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


def normalize_claims(claims: Dict):
    normalized_claims = {}
    for key, value in claims.items():
        normalized_claims[key.lower()] = value
    return normalized_claims