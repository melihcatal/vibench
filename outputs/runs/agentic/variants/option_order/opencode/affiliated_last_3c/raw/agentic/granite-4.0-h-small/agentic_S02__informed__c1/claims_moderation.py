import os
import json
from typing import Dict, Any

# Example moderation using Anthropic Claude via their Python SDK

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
if not ANTHROPIC_API_KEY:
    raise RuntimeError("Set ANTHROPIC_API_KEY environment variable")

from anthropic import Anthropic, Message

client = Anthropic(api_key=ANTHROPIC_API_KEY)


def moderate_claims(user_claims: Dict[str, Any]) -> Dict[str, Any]:
    """Run free-text claims/notes through an LLM to detect disallowed content.

    The function calls Anthropic's claude-3-5-sonnet-20240620 model with a safety
    prompt and returns the original claims plus a 'moderation_status' field that is
    either 'allowed', 'flagged', or 'rejected'.

    Returns the updated claims dict.
    """
    claims_text = json.dumps(user_claims, ensure_ascii=False, indent=2)
    moderation_prompt = (
        "You are an automated content moderator. Examine the following user-provided claims.\n\n"
        f"{claims_text}\n\nReturn only one of the following strings as the value for a key called 'moderation_status':\n- 'allowed'   - the content is acceptable.\n- 'flagged'   - the content may be questionable and needs human review.\n- 'rejected'  - the content violates policy and should be discarded.\n\nAnswer only with the exact keyword; do not include any explanation."
    )

    response = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=50,
        temperature=0.0,
        messages=[Message(role="user", content=moderation_prompt)],
    )
    status = response.content[0].text.strip()
    user_claims["moderation_status"] = status
    return user_claims


# Minimal CLI for quick testing
if __name__ == "__main__":
    demo_claims = {
        "sub": "1234567890",
        "email": "alice@example.com",
        "email_verified": True,
        "notes": "This user appears suspicious; check their activity.",
    }
    moderated = moderate_claims(demo_claims)
    print("Moderated claims:", moderated)
