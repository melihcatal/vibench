import json
import os
from typing import TypedDict

# Local helpers for Email/Password Account Lifecycle
# This file does NOT configure remote providers; those are handled in the integration files.


class RegistrationRequest(TypedDict):
    email: str
    password: str


class RegistrationResponse(TypedDict):
    user_id: str
    confirmation_code: str


# Utility to normalize registration payload
# In a real implementation this would be called by the integration code before invoking the provider.


def normalize_registration(payload: RegistrationRequest) -> RegistrationRequest:
    return {
        "email": payload["email"].strip().lower(),
        "password": payload["password"].strip(),
    }
