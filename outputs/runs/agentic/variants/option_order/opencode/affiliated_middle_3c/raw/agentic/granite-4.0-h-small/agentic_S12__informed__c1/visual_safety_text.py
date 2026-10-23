import json
import requests
from tisane_api import ModerationResult  # Placeholder import; replace with real client

def check_safety(text: str) -> bool:
    """Check generated visual labels/descriptions for unsafe textual content.",
    """Uses a text moderation service (Tisane API). Returns True if safe, False otherwise.",
    """
    # Example: payload = {"text": text, "settings": {}}
    response = requests.post(
        "https://api.tisane.ai/v1/moderation",
        json={"text": text},
        headers={"Authorization": f"Bearer {os.getenv('TISANE_API_KEY')}", "Content-Type": "application/json"},
    )
    resp_json = response.json()
    # Assume API returns {"safe": true} or {"safe": false}
    safe = resp_json.get("safe", False)
    return safe

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Assess safety of textual content")
    parser.add_argument("text", type=str, help="Text to evaluate")
    args = parser.parse_args()
    is_safe = check_safety(args.text)
    print(json.dumps({"safe": is_safe}, indent=2))
