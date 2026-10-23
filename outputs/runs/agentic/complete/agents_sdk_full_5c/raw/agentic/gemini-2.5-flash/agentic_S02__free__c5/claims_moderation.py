import os
import requests
import json

# OpenAI API configuration for Moderation
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "YOUR_OPENAI_API_KEY")
OPENAI_MODERATION_URL = "https://api.openai.com/v1/moderations"

def moderate_text_claim(text: str) -> dict | None:
    """Moderates a free-text claim using OpenAI's Moderation API."""
    if not OPENAI_API_KEY or "YOUR_OPENAI_API_KEY" in OPENAI_API_KEY:
        print("Error: OPENAI_API_KEY is not set.")
        return None

    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json",
    }

    data = {
        "input": text,
    }

    try:
        response = requests.post(OPENAI_MODERATION_URL, headers=headers, data=json.dumps(data))
        response.raise_for_status()
        moderation_result = response.json()
        return moderation_result
    except requests.exceptions.RequestException as e:
        print(f"Error calling OpenAI Moderation API: {e}")
        if response is not None:
            print(f"Response content: {response.text}")
        return None
    except KeyError as e:
        print(f"Error parsing OpenAI response: Missing key {e}. Response: {moderation_result}")
        return None

if __name__ == "__main__":
    print("Moderating claims...")

    claims_to_moderate = [
        "This is a perfectly normal user note about their preferences.",
        "I hate spam and phishing emails.",
        "I want to access all my data now!",
        "Kill all processes related to \'malicious_app\'.", # Example of a potentially problematic instruction
        "I will break all the rules and hack into the system!"
    ]

    for i, claim in enumerate(claims_to_moderate):
        print(f"\n--- Moderating Claim {i+1} ---")
        print(f"Original Claim: \"{claim}\"")
        result = moderate_text_claim(claim)

        if result and result.get("results"):
            mod_output = result["results"][0]
            print(f"Flagged: {mod_output["flagged"]}")
            if mod_output["flagged"]:
                print("Categories flagged:")
                for category, value in mod_output["categories"].items():
                    if value:
                        print(f"  - {category}: {mod_output["category_scores"][category]:.4f}")
        else:
            print("Failed to get moderation result.")
