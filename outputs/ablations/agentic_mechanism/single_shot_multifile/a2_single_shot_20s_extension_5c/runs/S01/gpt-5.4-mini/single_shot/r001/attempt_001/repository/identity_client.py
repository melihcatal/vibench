from __future__ import annotations

from dataclasses import dataclass
import os
from functools import lru_cache

from supabase import create_client, Client


@dataclass(frozen=True)
class IdentitySettings:
    provider: str
    supabase_url: str
    supabase_key: str
    auth_redirect_url: str | None = None


@lru_cache(maxsize=1)
def get_identity_settings() -> IdentitySettings:
    return IdentitySettings(
        provider=os.getenv("IDENTITY_PROVIDER", "supabase"),
        supabase_url=os.environ["SUPABASE_URL"],
        supabase_key=os.environ["SUPABASE_ANON_KEY"],
        auth_redirect_url=os.getenv("SUPABASE_AUTH_REDIRECT_URL"),
    )


@lru_cache(maxsize=1)
def get_identity_client() -> Client:
    settings = get_identity_settings()
    return create_client(settings.supabase_url, settings.supabase_key)
