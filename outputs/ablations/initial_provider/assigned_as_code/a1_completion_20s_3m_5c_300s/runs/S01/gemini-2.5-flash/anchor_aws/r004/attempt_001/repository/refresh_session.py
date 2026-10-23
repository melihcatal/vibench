import requests
import os

def refresh_session(refresh_token: str):
    api_key = os.environ.get("FIREBASE_API_KEY")
    rest_api_url = f"https://securetoken.googleapis.com/v1/token?key={api_key}"
    payload = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token
    }
    response = requests.post(rest_api_url, json=payload).json()
    if "error" in response:
        raise Exception(response["error"]["message"])
    return {"id_token": response["id_token"], "refresh_token": response["refresh_token"]}
