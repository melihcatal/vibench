import os
from safety_client import safety_client

def moderate_text(user_text: str, unsafe_threshold: float = 0.5) -> bool:
    """Score a single piece of text for unsafe or policy‑violating content using the OpenAI Moderation API.

    Returns True if the text is flagged as unsafe, False otherwise.
    """
    response = safety_client.create_moderation(input=user_text)
    flagged = any(
        result['flagged'] and result['flag_details'][category]['score'] >= unsafe_threshold
        for category, result in response['results'].items()
    )
    return flagged
