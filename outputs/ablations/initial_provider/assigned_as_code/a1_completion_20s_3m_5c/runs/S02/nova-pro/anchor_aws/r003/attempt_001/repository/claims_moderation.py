def claims_moderation(claims):
    moderated_claims = {}
    for key, value in claims.items():
        if key in ['email', 'name']:
            moderated_claims[key] = value
    return moderated_claims