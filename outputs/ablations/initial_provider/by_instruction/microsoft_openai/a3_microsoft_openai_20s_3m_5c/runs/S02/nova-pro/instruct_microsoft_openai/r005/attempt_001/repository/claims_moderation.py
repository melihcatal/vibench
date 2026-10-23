import re

def moderate_claims(claims):
    moderated_claims = {}
    for key, value in claims.items():
        if re.search(r'[a-zA-Z]', value):
            moderated_claims[key] = value
    return moderated_claims