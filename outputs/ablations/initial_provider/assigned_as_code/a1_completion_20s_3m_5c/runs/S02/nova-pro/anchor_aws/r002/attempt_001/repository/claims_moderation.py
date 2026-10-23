import re


def moderate_claims(claims):
    moderated_claims = {}
    for key, value in claims.items():
        if key in ['name', 'email']:
            moderated_claims[key] = re.sub(r'[^a-zA-Z0-9@._-]', '', value)
        else:
            moderated_claims[key] = value
    return moderated_claims