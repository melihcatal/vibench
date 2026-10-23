from identity_client import openai_headers, post_json


def refresh_session(refresh_token: str):
    payload = {"refresh_token": refresh_token, "grant_type": "refresh_token"}
    return post_json("https://api.openai.com/v1/auth/refresh", payload, headers=openai_headers())
