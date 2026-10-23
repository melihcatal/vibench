from __future__ import annotations

from typing import Any, Dict

from identity_client import Auth0Client
from identity_models import UserRecord, UserRegistration


def register_user(registration: UserRegistration) -> UserRecord:
    client = Auth0Client()
    data = client.create_database_user(registration.to_auth0_payload())
    return UserRecord.from_auth0(data)


def register_user_from_dict(payload: Dict[str, Any]) -> Dict[str, Any]:
    registration = UserRegistration(**payload)
    return register_user(registration).raw
