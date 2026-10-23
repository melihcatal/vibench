import os
import requests

# Configuration for Tisane text moderation service.
TISANE_ENDPOINT = os.getenv("TISANE_ENDPOINT", "https://api.tisane.ai/v2/parse")
TISANE_KEY = os.getenv("TISANE_API_KEY", "${TISANE_API_KEY}")

HEADERS = {
    "Authorization": f"Bearer {TISANE_KEY}",
    "Content-Type": "application/json"
}


def is_safe(text: str) -> bool:
    """
    Send the provided text to Tisane's moderation endpoint.
    Returns True if the content is considered safe, False otherwise.
    """
    payload = {
        "text": text,
        "settings": {
            "moderation": {
                "hate_speech": True,
                "sexual_content": True,
                "violence": True,
                "self_harm": True
            }
        }
    }
    response = requests.post(TISANE_ENDPOINT, headers=HEADERS, json=payload)
    if response.status_code != 200:
        raise RuntimeError(f"Tisane moderation failed: {response.status_code} {response.text}")
    result = response.json()
    # Tisane returns a list of issues under "issues"; safe if empty.
    issues = result.get("issues", [])
    return len(issues) == 0


def check_script_file(script_path: str) -> bool:
    """Read a script file and run safety check."""
    with open(script_path, "r", encoding="utf-8") as f:
        text = f.read()
    return is_safe(text)

# Example CLI (delete when importing as a module)
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Check narration script for unsafe content")
    parser.add_argument("script", help="Path to script file")
    args = parser.parse_args()
    safe = check_script_file(args.script)
    print("Script is safe" if safe else "Script contains unsafe content")
