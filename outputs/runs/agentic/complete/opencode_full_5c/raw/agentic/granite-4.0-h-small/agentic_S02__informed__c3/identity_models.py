import dataclasses

# Google Identity Platform OIDC reference
# service: Google Identity Platform
# interface: sdk_or_rest
# auth: GOOGLE_APPLICATION_CREDENTIALS


class UserInfo:
    def __init__(self, **kwargs):
        dataclasses.dataclass(self, **kwargs)


@dataclasses.dataclass
class NormalizedProfile:
    user_id: str
    email: str | None = None
    display_name: str | None = None
    avatar_url: str | None = None
    language: str | None = None
