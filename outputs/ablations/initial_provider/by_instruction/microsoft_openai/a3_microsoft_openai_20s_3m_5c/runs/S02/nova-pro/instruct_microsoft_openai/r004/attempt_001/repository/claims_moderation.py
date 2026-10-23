import re

def moderate_claims(claims):
    moderated_claims = {}
    for key, value in claims.items():
        if isinstance(value, str):
            value = re.sub(r'[^a-zA-Z0-9\s]', '', value)
        moderated_claims[key] = value
    return moderated_claims

if __name__ == '__main__':
    pass