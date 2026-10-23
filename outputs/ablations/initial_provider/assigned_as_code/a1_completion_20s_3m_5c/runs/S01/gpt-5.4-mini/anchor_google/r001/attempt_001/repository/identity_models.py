from dataclasses import dataclass


def normalize_email(email):
    return email.strip().lower()


@dataclass
class IdentityRequest:
    payload: dict

    def email(self):
        return normalize_email(self.payload["email"])

    def password(self):
        return self.payload.get("password")


@dataclass
class IdentityResponse:
    data: dict

    def as_dict(self):
        return self.data
