import os

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

import anthropic


def claims_moderation(claims):
    # Anthropic moderation of free-text claims
    pass
