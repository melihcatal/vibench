import dataclasses


@dataclasses.dataclass
class OAuthTokens:
    access_token: str
    id_token: str
    refresh_token: str | None = None
    expires_in: int | None = None
    token_type: str | None = None


@dataclasses.dataclass
class UserProfileClaims:
    sub: str
    email: str | None = None
    email_verified: bool | None = None
    name: str | None = None
    given_name: str | None = None
    family_name: str | None = None
    picture: str | None = None
    locale: str | None = None
