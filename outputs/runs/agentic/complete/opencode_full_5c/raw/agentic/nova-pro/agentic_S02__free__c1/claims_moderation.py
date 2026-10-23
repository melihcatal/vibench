def moderate_claims(claims):
    moderated_claims = {
        key: value.replace("badword", "***") for key, value in claims.items()
    }
    return moderated_claims
