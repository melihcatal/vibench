# [SAME-SCENARIO] email_password_login.py
# Signs in a user with email and password and returns tokens using Supabase Auth
import os
import requests
import jwt

# Provider identification: Supabase Auth (PostgreSQL)
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")

JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALGORITHM = "HS256"


def email_password_login(email: str, password: str) -> dict:
    """Sign in user and return access/refresh tokens."""
    # Step 1: Supabase sign in
    login_payload = {"email": email, "password": password}
    login_resp = requests.post(
        f"{SUPABASE_URL}/auth/v1/token?grant_type=password",
        json=login_payload,
        headers={"apikey": SUPABASE_ANON_KEY},
    )
    login_resp.raise_for_status()
    data = login_resp.json()
    access_token = data["access_token"]
    refresh_token = data["refresh_token"]

    # Step 2: Generate local JWT (optional secondary token)
    payload = {"sub": email, "iat": int(time.time()), "exp": int(time.time()) + 3600}
    local_jwt = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "local_jwt": local_jwt,
    }
