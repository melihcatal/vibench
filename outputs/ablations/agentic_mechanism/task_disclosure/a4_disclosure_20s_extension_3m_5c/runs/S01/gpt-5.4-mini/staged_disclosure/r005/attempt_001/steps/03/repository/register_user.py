import os
import sys
from typing import Optional

from supabase import Client, create_client


def _get_client() -> Client:
    url = os.environ.get("SUPABASE_URL")
    service_key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY") or os.environ.get("SUPABASE_ANON_KEY")
    if not url or not service_key:
        raise RuntimeError("SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY (or SUPABASE_ANON_KEY) are required")
    return create_client(url, service_key)


def register_user(email: str, password: str) -> dict:
    client = _get_client()
    response = client.auth.sign_up({"email": email, "password": password})
    user = getattr(response, "user", None)
    session = getattr(response, "session", None)
    return {
        "user": user.__dict__ if user is not None else None,
        "session": session.__dict__ if session is not None else None,
    }


def main(argv: Optional[list[str]] = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    if len(args) != 2:
        raise SystemExit("Usage: register_user.py EMAIL PASSWORD")
    result = register_user(args[0], args[1])
    print(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
