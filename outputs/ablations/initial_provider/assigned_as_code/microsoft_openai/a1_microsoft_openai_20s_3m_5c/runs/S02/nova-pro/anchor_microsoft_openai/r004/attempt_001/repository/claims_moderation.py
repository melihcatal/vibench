def moderate_claims(claims):
    moderated_claims = {}
    for key, value in claims.items():
        if isinstance(value, str):
            moderated_claims[key] = value.strip()
        else:
            moderated_claims[key] = value
    return moderated_claims