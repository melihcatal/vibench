from dataclasses import dataclass


@dataclass
class OAuthCallbackRequest:
    code: str
    redirect_uri: str
    code_verifier: str | None = None

    @classmethod
    def from_payload(cls, payload):
        return cls(
            code=payload["code"],
            redirect_uri=payload["redirect_uri"],
            code_verifier=payload.get("code_verifier"),
        )


@dataclass
class TokenResponse:
    access_token: str | None = None
    id_token: str | None = None
    refresh_token: str | None = None
    token_type: str | None = None
    expires_in: int | None = None

    @classmethod
    def from_dict(cls, data):
        return cls(
            access_token=data.get("access_token"),
            id_token=data.get("id_token"),
            refresh_token=data.get("refresh_token"),
            token_type=data.get("token_type"),
            expires_in=data.get("expires_in"),
        )

    def to_dict(self):
        return {
            "access_token": self.access_token,
            "id_token": self.id_token,
            "refresh_token": self.refresh_token,
            "token_type": self.token_type,
            "expires_in": self.expires_in,
        }


def normalize_profile_claims(claims):
    return {
        "subject": claims.get("sub"),
        "email": claims.get("email"),
        "email_verified": claims.get("email_verified"),
        "full_name": claims.get("name") or claims.get("preferred_username"),
        "given_name": claims.get("given_name"),
        "family_name": claims.get("family_name"),
        "locale": claims.get("locale"),
        "claims": claims,
    }
