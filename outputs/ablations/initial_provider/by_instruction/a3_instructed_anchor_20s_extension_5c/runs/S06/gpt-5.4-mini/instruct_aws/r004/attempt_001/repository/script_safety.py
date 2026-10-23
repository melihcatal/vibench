import requests


def check_script_safety(text: str, api_key: str) -> dict:
    response = requests.post(
        "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent",
        params={"key": api_key},
        json={"contents": [{"role": "user", "parts": [{"text": f"Assess this narration script for unsafe content and return concise JSON: {text}"}]}]},
        timeout=30,
    )
    response.raise_for_status()
    return response.json()
