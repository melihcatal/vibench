import re
from pydantic import BaseModel, Field

# Simple profanity filter (placeholder, replace with a real moderation service if needed)
PROFANITY_LIST = ["badword1", "badword2"]

class ModerateRequest(BaseModel):
    profile_text: str = Field(..., description="User-provided profile bio")

def profile_moderation(profile_text: str) -> str:
    """Moderates profile text before account activation.

    - Strips HTML tags
    - Removes or replaces profanity
    - Truncates to a reasonable length (e.g., 500 chars)
    """
    # Remove HTML tags
    clean = re.sub(r"<[^>]+>", "", profile_text)
    # Simple profanity replacement
    for profane in PROFANITY_LIST:
        clean = clean.replace(profane, "[censored]")
    # Truncate safely
    return clean[:500]