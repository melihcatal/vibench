class IdentityRequest:
    def __init__(self, data):
        self.data = data


class IdentityResponse:
    def __init__(self, data):
        self.data = data


def normalize_claims(claims):
    return claims
