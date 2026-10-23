from identity_client import get_userinfo
from identity_models import TokenResponse, UserInfo


def fetch_and_normalize_profile(tokens: TokenResponse) -> UserInfo:
    raw_profile = get_userinfo(tokens["access_token"])
    # Normalization: ensure keys present, defaults if missing
    normalized: UserInfo = {
        "sub": raw_profile["sub"],
        "name": raw_profile.get("name"),
        "given_name": raw_profile.get("given_name"),
        "family_name": raw_profile.get("family_name"),
        "email": raw_profile.get("email"),
        "email_verified": raw_profile.get("email_verified"),
    }
    return normalized


if __name__ == "__main__":
    pass
