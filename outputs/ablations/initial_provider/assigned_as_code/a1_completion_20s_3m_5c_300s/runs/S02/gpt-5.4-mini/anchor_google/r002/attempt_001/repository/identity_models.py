from dataclasses import dataclass


@dataclass
class OAuthStartRequest:
    redirect_uri: str


@dataclass
class OAuthCallbackRequest:
    code: str
    redirect_uri: str


@dataclass
class PKCELoginRequest:
    redirect_uri: str
    code_verifier: str


def merge_claims(base, override=None):
    override = override or {}
    result = dict(base)
    for key, value in override.items():
        if value is not None:
            result[key] = value
    return result
