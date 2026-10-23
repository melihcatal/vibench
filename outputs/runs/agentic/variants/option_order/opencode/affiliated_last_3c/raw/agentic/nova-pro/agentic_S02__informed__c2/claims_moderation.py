import re


# Moderate free-text claims or notes
def moderate_claims(claims):
    moderated_claims = []
    for claim in claims:
        if not re.search(r"\b(badword1|badword2)\b", claim, re.IGNORECASE):
            moderated_claims.append(claim)
    return moderated_claims
