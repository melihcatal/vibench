import re


def moderate_claims(claims: str):
    moderated_claims = re.sub(r"[^a-zA-Z0-9\s]", "", claims)
    return moderated_claims


if __name__ == "__main__":
    claims = "User@123! claims"
    print(moderate_claims(claims))
